"""Command line interface for Project MAMMAL scientific instrument."""

from __future__ import annotations

import sys
from pathlib import Path

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from mammal import __version__
from mammal.artifacts.store import ArtifactStore
from mammal.config import settings
from mammal.db import check_db, get_engine, get_session, init_db

console = Console()


@click.group()
@click.version_option(version=__version__, prog_name="mammal")
def main() -> None:
    """Project MAMMAL: Scientific instrument & provenance kernel."""
    pass


@main.command()
def doctor() -> None:
    """Run environmental diagnostics, directory validation, and database health checks."""
    console.print(Panel(f"[bold cyan]Project MAMMAL Diagnostic Doctor (v{__version__})[/bold cyan]"))

    table = Table(title="System Environment & Configuration", show_header=True, header_style="bold magenta")
    table.add_column("Component", style="cyan")
    table.add_column("Status / Path", style="green")

    table.add_row("Python Version", sys.version.split()[0])
    table.add_row("Data Root (MAMMAL_DATA_ROOT)", str(settings.data_root))
    table.add_row("Database Path", str(settings.db_path))

    # Ensure directories exist
    settings.ensure_directories()
    table.add_row("Data Directories", "INITIALIZED / OK")

    # Check DB
    try:
        engine = get_engine()
        init_db(engine)
        db_status = check_db(engine)
        table.add_row("SQLite Foreign Keys", db_status["foreign_keys"])
        table.add_row("SQLite Journal Mode", db_status["journal_mode"])
        table.add_row("SQLite Integrity Check", db_status["integrity"])
    except Exception as exc:
        table.add_row("Database Status", f"[red]ERROR: {exc}[/red]")

    # Check Artifacts
    try:
        store = ArtifactStore()
        with get_session() as session:
            art_status = store.verify_all_artifacts(session)
            table.add_row(
                "Artifact Store",
                f"{art_status['verified']}/{art_status['total']} verified ({art_status['status']})"
            )
    except Exception as exc:
        table.add_row("Artifact Store", f"[red]ERROR: {exc}[/red]")

    console.print(table)


@main.group()
def db() -> None:
    """Database administration commands."""
    pass


@db.command(name="init")
def db_init() -> None:
    """Initialize database tables."""
    settings.ensure_directories()
    init_db()
    console.print(f"[bold green]✓ Database initialized successfully at {settings.db_path}[/bold green]")


@db.command(name="check")
def db_check() -> None:
    """Run database integrity checks."""
    status = check_db()
    table = Table(title="Database Health Check", show_header=True, header_style="bold blue")
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="green" if status["integrity"] == "ok" else "red")

    for k, v in status.items():
        table.add_row(k, v)

    console.print(table)


@main.group()
def artifacts() -> None:
    """Artifact store commands."""
    pass


@artifacts.command(name="verify")
def artifacts_verify() -> None:
    """Verify cryptographic hashes for all artifacts on disk."""
    store = ArtifactStore()
    with get_session() as session:
        result = store.verify_all_artifacts(session)

    table = Table(title="Artifact Verification Audit", show_header=True, header_style="bold yellow")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green" if result["status"] == "PASS" else "red")

    table.add_row("Total Registered", str(result["total"]))
    table.add_row("Verified Intact", str(result["verified"]))
    table.add_row("Missing Files", str(len(result["missing"])))
    table.add_row("Corrupted Files", str(len(result["corrupted"])))
    table.add_row("Audit Result", result["status"])

    console.print(table)


@main.command(name="replay")
@click.argument("episode_id", required=False)
@click.option("--all", "replay_all", is_flag=True, default=False, help="Replay all recorded episodes.")
def cli_replay(episode_id: str | None, replay_all: bool) -> None:
    """Reconstruct trial states and verify SHA-256 event chains for an episode."""
    from mammal.config import Settings
    from mammal.models.entities import Episode
    from mammal.trials.replay import replay_session_from_events

    app_settings = Settings.load()
    with get_session(app_settings) as session:
        if replay_all:
            episodes = session.query(Episode).all()
            target_ids = [ep.id for ep in episodes]
        elif episode_id:
            target_ids = [episode_id]
        else:
            console.print("[red]Error: Please specify an episode_id or pass --all[/red]")
            return

        if not target_ids:
            console.print("[yellow]No episodes found to replay.[/yellow]")
            return

        for ep_id in target_ids:
            try:
                summary = replay_session_from_events(session, ep_id, app_settings=app_settings)
                status_str = "[bold green]PASS[/bold green]" if summary.is_valid else "[bold red]FAIL[/bold red]"
                console.print(Panel(f"Session Replay Audit: [cyan]{ep_id}[/cyan] &mdash; Result: {status_str}"))

                table = Table(show_header=True, header_style="bold blue")
                table.add_column("Property", style="cyan")
                table.add_column("Value", style="green" if summary.is_valid else "red")
                table.add_row("Total Trials", str(summary.total_trials))
                table.add_row("Replayed Trials", str(summary.replayed_trials))
                table.add_row("Total Events Verified", str(summary.total_events))
                table.add_row("Artifacts Verified", str(summary.total_artifacts_verified))
                table.add_row("Chain Integrity", "VALID (100% SHA-256 MATCH)" if summary.is_valid else "CORRUPTED")

                console.print(table)
                if summary.discrepancies:
                    console.print("[bold red]Discrepancies found:[/bold red]")
                    for disc in summary.discrepancies:
                        console.print(f"  [red]&bull; {disc}[/red]")
            except Exception as exc:
                console.print(f"[bold red]Replay error for {ep_id}: {exc}[/bold red]")


@main.command(name="export")
@click.argument("episode_id")
@click.argument("output_path", type=click.Path(dir_okay=False))
def cli_export(episode_id: str, output_path: str) -> None:
    """Export complete episode data and artifacts to a portable .tar.gz archive."""
    from mammal.backup.archive import export_session_archive
    from mammal.config import Settings

    app_settings = Settings.load()
    with get_session(app_settings) as session:
        try:
            out_file = export_session_archive(session, episode_id, output_path, app_settings=app_settings)
            console.print(f"[bold green]✓ Episode {episode_id} exported successfully to {out_file}[/bold green]")
        except Exception as exc:
            console.print(f"[bold red]Export failed: {exc}[/bold red]")


@main.command(name="restore")
@click.argument("archive_path", type=click.Path(exists=True, dir_okay=False))
def cli_restore(archive_path: str) -> None:
    """Restore a session archive and verify its cryptographic integrity."""
    from mammal.backup.archive import restore_session_archive
    from mammal.config import Settings
    from mammal.trials.replay import replay_session_from_events

    app_settings = Settings.load()
    try:
        ep_id = restore_session_archive(archive_path, app_settings)
        console.print(f"[bold green]✓ Session archive restored successfully (Episode: {ep_id})[/bold green]")

        with get_session(app_settings) as session:
            summary = replay_session_from_events(session, ep_id, app_settings=app_settings)
            if summary.is_valid:
                console.print(f"[bold green]✓ Replay verification passed on restored session {ep_id}[/bold green]")
            else:
                console.print(f"[bold red]⚠ Replay verification reported discrepancies on {ep_id}[/bold red]")
    except Exception as exc:
        console.print(f"[bold red]Restore failed: {exc}[/bold red]")


@main.command(name="seed")
def cli_seed() -> None:
    """Seed qualification and baseline items into the item bank."""
    from mammal.config import Settings
    from mammal.items.bank import seed_qualification_items

    app_settings = Settings.load()
    with get_session(app_settings) as session:
        items = seed_qualification_items(session)
        session.commit()
        console.print(f"[bold green]✓ Successfully seeded {len(items)} items into item bank.[/bold green]")


@main.command(name="analyze")
@click.argument("episode_id")
@click.option("--format", "output_format", type=click.Choice(["text", "markdown", "json"]), default="text", help="Output format.")
def cli_analyze(episode_id: str, output_format: str) -> None:
    """Run statistical analysis and compute accuracy, Brier, ECE, and Type-2 SDT metrics."""
    from mammal.analysis.engine import generate_analysis_report
    from mammal.config import Settings

    app_settings = Settings.load()
    with get_session(app_settings) as session:
        try:
            report_data = generate_analysis_report(session, episode_id, app_settings=app_settings)
            res = report_data["result"]

            if output_format == "json":
                import json
                from dataclasses import asdict
                console.print(json.dumps(asdict(res), indent=2))
            elif output_format == "markdown":
                console.print(report_data["markdown_text"])
            else:
                console.print(Panel(f"[bold cyan]MAMMAL Statistical Analysis &mdash; Episode {episode_id}[/bold cyan]"))
                table = Table(title="Empirical Estimands (with 95% Block Bootstrap CI)", show_header=True, header_style="bold blue")
                table.add_column("Estimand", style="cyan")
                table.add_column("Point Estimate", style="bold green")
                table.add_column("95% Empirical CI", style="yellow")

                table.add_row("Accuracy", f"{res.accuracy.estimate * 100:.1f}%", f"[{res.accuracy.ci_lower * 100:.1f}%, {res.accuracy.ci_upper * 100:.1f}%]")
                table.add_row("Brier Score", f"{res.brier_score.estimate:.4f}", f"[{res.brier_score.ci_lower:.4f}, {res.brier_score.ci_upper:.4f}]")
                table.add_row("Expected Calibration Error (ECE)", f"{res.ece.estimate:.4f}", f"[{res.ece.ci_lower:.4f}, {res.ece.ci_upper:.4f}]")
                table.add_row("Type-2 AUROC (AUROC2)", f"{res.auroc2.estimate:.4f}", f"[{res.auroc2.ci_lower:.4f}, {res.auroc2.ci_upper:.4f}]")
                table.add_row("First-order Sensitivity (d')", f"{res.d_prime:.3f}", "—")
                table.add_row("Metacognitive Sensitivity (meta-d')", f"{res.meta_d_prime:.3f}", "—")
                table.add_row("Metacognitive Efficiency (M_ratio)", f"{res.m_ratio:.3f}", "—")

                console.print(table)
                console.print(f"[green]✓ Derived JSON report saved to {report_data['json_artifact'].rel_path}[/green]")
                console.print(f"[green]✓ Derived Markdown report saved to {report_data['markdown_artifact'].rel_path}[/green]")
        except Exception as exc:
            console.print(f"[bold red]Analysis failed: {exc}[/bold red]")


@main.command(name="plan-precision")
@click.option("--metric", default="brier", type=click.Choice(["brier", "accuracy", "auroc2"]), help="Target estimand metric.")
@click.option("--ci-half-width", default=0.05, type=float, help="Target 95% confidence interval half-width.")
@click.option("--base-rate", default=0.75, type=float, help="Assumed accuracy base rate.")
def cli_plan_precision(metric: str, ci_half_width: float, base_rate: float) -> None:
    """Run Monte Carlo simulation power analysis to compute required trial sample sizes."""
    from mammal.analysis.precision_planner import plan_session_precision

    result = plan_session_precision(
        target_metric=metric,
        target_ci_half_width=ci_half_width,
        assumed_base_rate=base_rate,
    )

    console.print(Panel(f"[bold cyan]MAMMAL Precision Planner // Target Metric: {metric.upper()}[/bold cyan]\nGoal: 95% CI Half-Width &le; {ci_half_width:.3f} (Total Width &le; {ci_half_width*2:.3f})"))

    table = Table(title="Monte Carlo Sample Size Simulations", show_header=True, header_style="bold blue")
    table.add_column("Sample Size (N)", style="cyan")
    table.add_column("Mean 95% CI Width", style="yellow")
    table.add_column("Standard Error", style="dim")
    table.add_column("Status", style="bold")

    for rec in result.recommendations:
        status_txt = "[green]MEETS TARGET[/green]" if rec.meets_criterion else "[dim]Insufficient[/dim]"
        table.add_row(
            str(rec.sample_size),
            f"{rec.mean_ci_width:.4f}",
            f"{rec.standard_error:.4f}",
            status_txt,
        )

    console.print(table)
    console.print(f"[bold green]✓ Recommended minimum sample size: N = {result.recommended_sample_size} trials[/bold green]")


@main.command(name="freeze-manifest")
@click.argument("episode_id")
def cli_freeze_manifest(episode_id: str) -> None:
    """Freeze a completed human session into an immutable target dataset for observers."""
    from mammal.analysis.manifest import create_frozen_target_manifest
    from mammal.config import Settings

    app_settings = Settings.load()
    with get_session(app_settings) as session:
        try:
            res = create_frozen_target_manifest(session, episode_id, app_settings=app_settings)
            m = res["manifest"]
            art = res["artifact"]

            console.print(Panel(f"[bold green]✓ Target Manifest Frozen Successfully[/bold green]"))
            console.print(f"[cyan]Episode ID:[/cyan] {m.episode_id}")
            console.print(f"[cyan]Total Trials:[/cyan] {m.total_trials}")
            console.print(f"[cyan]Manifest SHA-256 Digest:[/cyan] {m.manifest_hash}")
            console.print(f"[cyan]Artifact Path:[/cyan] {art.rel_path}")
        except Exception as exc:
            console.print(f"[bold red]Failed to freeze manifest: {exc}[/bold red]")


@main.command(name="observe")
@click.argument("episode_id")
@click.option("--observer", "-o", default="item_base_rate", help="Observer identifier (uniform_chance, item_base_rate, deterministic_solver, text_confidence_heuristic).")
def cli_observe(episode_id: str, observer: str) -> None:
    """Run an external/statistical observer across a frozen session manifest."""
    from mammal.config import Settings
    from mammal.observers.runner import get_observer, run_observer_on_episode

    app_settings = Settings.load()
    with get_session(app_settings) as session:
        try:
            obs = get_observer(observer)
            res = run_observer_on_episode(session, episode_id, obs, app_settings=app_settings)
            preds = res["predictions"]
            art = res["artifact"]

            console.print(Panel(f"[bold cyan]MAMMAL Observer Evaluation // {obs.observer_id} (v{obs.version})[/bold cyan]\nVisibility Contract: [yellow]{obs.visibility_level.value}[/yellow]"))
            console.print(f"[green]✓ Completed {len(preds)} trial predictions[/green]")
            console.print(f"[green]✓ Saved observer run artifact: {art.rel_path}[/green]")
        except Exception as exc:
            console.print(f"[bold red]Observer execution failed: {exc}[/bold red]")


@main.command(name="compare")
@click.argument("episode_id")
@click.option("--observer", "-o", default="item_base_rate", help="Observer identifier to compare against Self.")
def cli_compare(episode_id: str, observer: str) -> None:
    """Perform paired statistical comparison (Self vs. Observer) and compute PAI."""
    from mammal.config import Settings
    from mammal.observers.runner import get_observer, run_observer_on_episode

    app_settings = Settings.load()
    with get_session(app_settings) as session:
        try:
            obs = get_observer(observer)
            res = run_observer_on_episode(session, episode_id, obs, app_settings=app_settings)
            p = res["paired_result"]
            if not p:
                console.print("[bold yellow]No paired confidence ratings available for comparison.[/bold yellow]")
                return

            console.print(Panel(f"[bold cyan]MAMMAL Paired Comparison // Self vs. {obs.observer_id}[/bold cyan]"))
            table = Table(title="Paired Performance & Metacognitive Estimands (with 95% Bootstrap CI)", show_header=True, header_style="bold blue")
            table.add_column("Estimand", style="cyan")
            table.add_column("Self", style="bold green")
            table.add_column("Observer", style="bold yellow")
            table.add_column("Paired Difference (\u0394)", style="magenta")
            table.add_column("95% Empirical CI", style="dim")

            table.add_row(
                "Brier Score (lower is better)",
                f"{p.self_brier:.4f}",
                f"{p.observer_brier:.4f}",
                f"\u0394 = {p.delta_brier:+.4f}",
                f"[{p.delta_brier_ci[0]:+.4f}, {p.delta_brier_ci[1]:+.4f}]",
            )
            table.add_row(
                "Type-2 AUROC (higher is better)",
                f"{p.self_auroc2:.4f}",
                f"{p.observer_auroc2:.4f}",
                f"\u0394 = {p.delta_auroc2:+.4f}",
                f"[{p.delta_auroc2_ci[0]:+.4f}, {p.delta_auroc2_ci[1]:+.4f}]",
            )
            table.add_row(
                "Participant Advantage Index (PAI)",
                "—",
                "—",
                f"PAI = {p.participant_advantage_index:+.4f}",
                f"[{p.pai_ci[0]:+.4f}, {p.pai_ci[1]:+.4f}]",
            )

            console.print(table)
        except Exception as exc:
            console.print(f"[bold red]Comparison failed: {exc}[/bold red]")


@main.command(name="extract-acoustics")
@click.argument("episode_id")
def cli_extract_acoustics(episode_id: str) -> None:
    """Extract prosodic pitch, jitter, shimmer, and SNR features from recorded trial audio."""
    import json
    from dataclasses import asdict
    from mammal.artifacts.store import ArtifactStore
    from mammal.config import Settings
    from mammal.events.engine import EventEngine
    from mammal.models.entities import Artifact, Trial
    from mammal.processors.acoustics import extract_acoustic_features

    app_settings = Settings.load()
    with get_session(app_settings) as session:
        try:
            trials = session.query(Trial).filter(Trial.episode_id == episode_id).all()
            store = ArtifactStore(app_settings)
            event_engine = EventEngine(session)
            extracted_count = 0

            console.print(Panel(f"[bold cyan]MAMMAL Acoustic Feature Extraction // Episode {episode_id}[/bold cyan]"))

            for trial in trials:
                # Check for raw audio artifact
                audio_art = (
                    session.query(Artifact)
                    .filter(Artifact.rel_path.like(f"raw/audio/{trial.id}_%"))
                    .first()
                )
                if not audio_art:
                    continue

                audio_bytes = store.read_artifact_bytes(session, audio_art.artifact_id)
                features = extract_acoustic_features(audio_bytes, trial_id=trial.id)

                # Save derived acoustic features artifact
                feat_dict = asdict(features)
                art = store.save_derived_artifact(
                    session=session,
                    content=json.dumps(feat_dict, indent=2).encode("utf-8"),
                    mime_type="application/json",
                    category="derived/acoustics",
                    filename=f"{trial.id}_features.json",
                    source_artifact_ids=[audio_art.artifact_id],
                    processor_version="acoustics-dsp-v1.0",
                )

                # Log acoustic.extracted event
                event_engine.record_event(
                    trial_id=trial.id,
                    episode_id=episode_id,
                    event_type="acoustic.extracted",
                    actor="processor:acoustics",
                    payload={
                        "artifact_id": art.artifact_id,
                        "mean_f0_hz": features.mean_f0_hz,
                        "pitch_jitter_pct": features.pitch_jitter_pct,
                        "snr_db": features.quality_report.snr_db,
                        "is_passed": features.quality_report.is_passed,
                    },
                )
                extracted_count += 1

            session.commit()
            console.print(f"[bold green]✓ Successfully extracted acoustic features for {extracted_count} spoken trials[/bold green]")
        except Exception as exc:
            console.print(f"[bold red]Acoustic extraction failed: {exc}[/bold red]")


@main.command(name="audio-gain")
@click.argument("episode_id")
def cli_audio_gain(episode_id: str) -> None:
    """Analyze Audio Leakage Gain (comparing Text-only vs. Acoustic Prosody observers)."""
    from mammal.analysis.audio_gain import compute_audio_leakage_gain
    from mammal.config import Settings
    from mammal.observers.runner import get_observer, run_observer_on_episode

    app_settings = Settings.load()
    with get_session(app_settings) as session:
        try:
            # 1. Run Text Heuristic Observer
            obs_text = get_observer("text_confidence_heuristic")
            res_text = run_observer_on_episode(session, episode_id, obs_text, app_settings=app_settings)
            p_text = res_text["paired_result"]

            # 2. Run Acoustic Prosody Observer
            obs_audio = get_observer("acoustic_prosody")
            res_audio = run_observer_on_episode(session, episode_id, obs_audio, app_settings=app_settings)
            p_audio = res_audio["paired_result"]

            if not p_text or not p_audio:
                console.print("[bold yellow]Insufficient confidence ratings to compute audio gain.[/bold yellow]")
                return

            gain = compute_audio_leakage_gain(
                episode_id=episode_id,
                text_brier=p_text.observer_brier,
                acoustic_brier=p_audio.observer_brier,
                text_auroc2=p_text.observer_auroc2,
                acoustic_auroc2=p_audio.observer_auroc2,
            )

            console.print(Panel(f"[bold cyan]MAMMAL Public Signal & Audio Leakage Gain // Episode {episode_id}[/bold cyan]"))
            table = Table(title="Acoustic vs. Text Metacognitive Signal Gain", show_header=True, header_style="bold blue")
            table.add_column("Channel", style="cyan")
            table.add_column("Brier Score", style="bold yellow")
            table.add_column("Type-2 AUROC", style="bold green")

            table.add_row("Text-Only Channel", f"{gain.text_observer_brier:.4f}", f"{gain.text_auroc2:.4f}")
            table.add_row("Acoustic Prosody Channel", f"{gain.acoustic_observer_brier:.4f}", f"{gain.acoustic_auroc2:.4f}")
            table.add_row("Audio Leakage Gain (%)", f"{gain.audio_leakage_gain_pct:+.2f}%", f"\u0394 AUROC2 = {gain.delta_auroc2_gain:+.4f}")

            console.print(table)
            console.print(f"[bold green]Interpretation:[/bold green] {gain.public_signal_verdict}")
        except Exception as exc:
            console.print(f"[bold red]Audio gain analysis failed: {exc}[/bold red]")


@main.command(name="personalize")
@click.argument("episode_id")
def cli_personalize(episode_id: str) -> None:
    """Execute personalized prequential observer on an episode incorporating causal history."""
    from mammal.config import Settings
    from mammal.observers.runner import get_observer, run_observer_on_episode

    app_settings = Settings.load()
    with get_session(app_settings) as session:
        try:
            obs = get_observer("personalized_prequential")
            res = run_observer_on_episode(session, episode_id, obs, app_settings=app_settings)
            preds = res["predictions"]
            art = res["artifact"]

            console.print(Panel(f"[bold cyan]MAMMAL Personalized Prequential Observer // Episode {episode_id}[/bold cyan]"))
            console.print(f"[green]✓ Completed {len(preds)} personalized trial predictions[/green]")
            console.print(f"[green]✓ Saved run artifact: {art.rel_path}[/green]")
        except Exception as exc:
            console.print(f"[bold red]Personalized observer failed: {exc}[/bold red]")


@main.command(name="personalization-gain")
@click.argument("episode_id")
@click.option("--baseline", "-b", default="item_base_rate", help="Generic baseline observer to compare against.")
def cli_personalization_gain(episode_id: str, baseline: str) -> None:
    """Evaluate Personalization Gain (comparing Generic vs. Personalized observers across matched trials)."""
    from mammal.analysis.personalization_gain import compute_personalization_gain
    from mammal.config import Settings
    from mammal.models.entities import Episode, Trial
    from mammal.observers.runner import get_observer, run_observer_on_episode

    app_settings = Settings.load()
    with get_session(app_settings) as session:
        try:
            episode = session.get(Episode, episode_id)
            participant_id = episode.participant_id if episode else "unknown"

            # 1. Run Generic Baseline Observer
            obs_gen = get_observer(baseline)
            res_gen = run_observer_on_episode(session, episode_id, obs_gen, app_settings=app_settings)

            # 2. Run Personalized Prequential Observer
            obs_pers = get_observer("personalized_prequential")
            res_pers = run_observer_on_episode(session, episode_id, obs_pers, app_settings=app_settings)

            gen_confs = [p.confidence for p in res_gen["predictions"]]
            pers_confs = [p.confidence for p in res_pers["predictions"]]

            # Query real outcomes from trials
            trials = session.query(Trial).filter(Trial.episode_id == episode_id).order_by(Trial.trial_index.asc()).all()
            real_outcomes = [t.outcome.is_correct for t in trials if t.outcome is not None]

            if not real_outcomes:
                console.print("[bold yellow]No completed trials with outcomes found.[/bold yellow]")
                return

            gain_report = compute_personalization_gain(
                episode_id=episode_id,
                participant_id=participant_id,
                generic_observer_id=baseline,
                generic_confidences=gen_confs[:len(real_outcomes)],
                personalized_confidences=pers_confs[:len(real_outcomes)],
                outcomes=real_outcomes,
            )

            console.print(Panel(f"[bold cyan]MAMMAL Personalization Gain (Gate E05) // Episode {episode_id}[/bold cyan]"))
            table = Table(title="Generic vs. Personalized Observer Comparison (with 95% Bootstrap CI)", show_header=True, header_style="bold blue")
            table.add_column("Model", style="cyan")
            table.add_column("Brier Score", style="bold yellow")
            table.add_column("Type-2 AUROC", style="bold green")
            table.add_column("Personalization Gain (\u0394)", style="magenta")
            table.add_column("95% Empirical CI", style="dim")

            table.add_row(
                f"Generic Baseline ({baseline})",
                f"{gain_report.generic_brier:.4f}",
                f"{gain_report.generic_auroc2:.4f}",
                "—",
                "—",
            )
            table.add_row(
                "Personalized Prequential",
                f"{gain_report.personalized_brier:.4f}",
                f"{gain_report.personalized_auroc2:.4f}",
                f"\u0394 Brier = {gain_report.delta_brier_gain:+.4f}",
                f"[{gain_report.delta_brier_gain_ci[0]:+.4f}, {gain_report.delta_brier_gain_ci[1]:+.4f}]",
            )

            console.print(table)
            console.print(f"[bold green]Statement (AGENTS.md Rule 5):[/bold green]\n{gain_report.epistemic_statement}")
        except Exception as exc:
            console.print(f"[bold red]Personalization gain evaluation failed: {exc}[/bold red]")


@main.command(name="memory-analyze")
@click.argument("episode_id")
def cli_memory_analyze(episode_id: str) -> None:
    """Analyze prospective memory Judgments of Learning (JOLs) against future cued recall."""
    from mammal.config import Settings
    from mammal.memory.engine import analyze_memory_episode

    app_settings = Settings.load()
    with get_session(app_settings) as session:
        try:
            res = analyze_memory_episode(session, episode_id, app_settings=app_settings)
            an = res["analysis"]
            art = res["artifact"]

            console.print(Panel(f"[bold cyan]MAMMAL Future-Memory & JOL Metacognition // Episode {episode_id}[/bold cyan]"))
            table = Table(title="Prospective Memory Resolution Estimands", show_header=True, header_style="bold blue")
            table.add_column("Estimand", style="cyan")
            table.add_column("Value", style="bold green")
            table.add_column("Interpretation", style="yellow")

            table.add_row("Total Paired Associates", str(an.total_pairs), "Number of encoding-recall pairs")
            table.add_row("Cued Recall Accuracy", f"{an.recall_accuracy * 100:.1f}%", "Empirical future recall rate")
            table.add_row("Mean JOL Forecast", f"{an.mean_jol:.1f}%", "Average prospective confidence forecast")
            table.add_row("Goodman-Kruskal Gamma (\u03b3)", f"{an.gamma_correlation:+.4f}", "Rank correlation between JOL and recall")
            table.add_row("Prospective Type-2 AUROC", f"{an.prospective_auroc:.4f}", "Discrimination of future recall from JOL")
            table.add_row("Prospective Brier Score", f"{an.prospective_brier_score:.4f}", "Quadratic error of memory forecasts")

            console.print(table)
            console.print(f"[green]✓ Saved memory analysis artifact: {art.rel_path}[/green]")
        except Exception as exc:
            console.print(f"[bold red]Memory analysis failed: {exc}[/bold red]")


@main.command(name="audit-interventions")
@click.argument("episode_id")
def cli_audit_interventions(episode_id: str) -> None:
    """Audit all intervention delivery events and verify S3/Venom rule compliance."""
    from mammal.config import Settings
    from mammal.interventions.governance import InterventionGovernanceGuard
    from mammal.models.entities import Episode, TrialEvent

    app_settings = Settings.load()
    with get_session(app_settings) as session:
        try:
            episode = session.get(Episode, episode_id)
            if not episode:
                console.print(f"[bold red]Episode {episode_id} not found.[/bold red]")
                return

            events = (
                session.query(TrialEvent)
                .filter(TrialEvent.episode_id == episode_id, TrialEvent.event_type.like("intervention.%"))
                .order_by(TrialEvent.occurred_at.asc())
                .all()
            )

            console.print(Panel(f"[bold cyan]MAMMAL Intervention Governance Audit // Episode {episode_id}[/bold cyan]\nSession Mode: [yellow]{episode.mode.upper()}[/yellow]"))

            if not events:
                console.print("[dim]No intervention events recorded for this session.[/dim]")
                return

            table = Table(title="Intervention Event Log & Provenance", show_header=True, header_style="bold blue")
            table.add_column("Event ID", style="cyan")
            table.add_column("Trial", style="dim")
            table.add_column("Type", style="bold yellow")
            table.add_column("Model / Actor", style="green")
            table.add_column("Governance Status", style="magenta")

            for e in events:
                payload = e.payload_json or {}
                content = payload.get("content_text", "")
                gov = InterventionGovernanceGuard.validate_intervention(
                    message=content,
                    session_mode=episode.mode,
                    protocol_allows_feedback=(episode.mode == "intervention"),
                )
                status = "[green]COMPLIANT[/green]" if gov.is_approved else "[bold red]NON-COMPLIANT[/bold red]"
                table.add_row(e.event_id[:12], e.trial_id[:12] if e.trial_id else "—", e.event_type, e.actor, status)

            console.print(table)
        except Exception as exc:
            console.print(f"[bold red]Intervention audit failed: {exc}[/bold red]")


@main.command(name="intervention-effects")
@click.argument("episode_id")
def cli_intervention_effects(episode_id: str) -> None:
    """Analyze behavioral and metacognitive shifts induced by model interventions."""
    from mammal.analysis.intervention_effects import compute_intervention_effects
    from mammal.config import Settings

    app_settings = Settings.load()
    with get_session(app_settings) as session:
        try:
            report = compute_intervention_effects(session, episode_id)

            console.print(Panel(f"[bold cyan]MAMMAL Intervention Effects // Episode {episode_id}[/bold cyan]"))
            table = Table(title="Observation Baseline vs. Intervention Comparison", show_header=True, header_style="bold blue")
            table.add_column("Phase", style="cyan")
            table.add_column("Trials", style="dim")
            table.add_column("Accuracy", style="bold green")
            table.add_column("ECE (Calibration Error)", style="bold yellow")
            table.add_column("Brier Loss", style="magenta")

            table.add_row(
                "Baseline (Unassisted)",
                str(report.baseline_trials_count),
                f"{report.baseline_accuracy * 100:.1f}%",
                f"{report.baseline_ece:.4f}",
                f"{report.baseline_brier:.4f}",
            )
            table.add_row(
                "Intervention (Assisted)",
                str(report.intervention_trials_count),
                f"{report.intervention_accuracy * 100:.1f}%",
                f"{report.intervention_ece:.4f}",
                f"{report.intervention_brier:.4f}",
            )
            table.add_row(
                "Intervention Shift (\u0394)",
                "—",
                f"\u0394 Acc = {(report.intervention_accuracy - report.baseline_accuracy) * 100:+.1f}%",
                f"\u0394 ECE = {report.delta_ece_improvement:+.4f}",
                f"\u0394 Brier = {report.delta_brier_improvement:+.4f}",
            )

            console.print(table)
            console.print(f"[bold yellow]{report.rule6_epistemic_warning}[/bold yellow]")
        except Exception as exc:
            console.print(f"[bold red]Intervention effects analysis failed: {exc}[/bold red]")


@main.command()
@click.option("--host", default="127.0.0.1", help="Host interface to bind.")
@click.option("--port", default=5000, type=int, help="Port to listen on.")
@click.option("--debug", is_flag=True, default=False, help="Run in Flask debug mode.")
def serve(host: str, port: int, debug: bool) -> None:
    """Start Project MAMMAL local web server and session runner."""
    from mammal.app import create_app

    app = create_app()
    console.print(Panel(f"[bold cyan]MAMMAL POD // CODEC Session Server[/bold cyan]\nListening on [bold green]http://{host}:{port}[/bold green]"))
    app.run(host=host, port=port, debug=debug)


if __name__ == "__main__":
    main()







