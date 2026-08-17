"""Unit tests for domain session scheduler and multi-block balancing."""

from __future__ import annotations

from sqlalchemy.orm import Session

from mammal.items.bank import seed_qualification_items
from mammal.protocols.loader import load_and_register_all_protocols
from mammal.trials.scheduler import DomainSessionScheduler


def test_domain_session_scheduler_block_interleaving(session: Session):
    load_and_register_all_protocols(session)
    seed_qualification_items(session)

    scheduler = DomainSessionScheduler(session)
    domains = ["world_geography", "propositional_logic"]

    plan = scheduler.plan_session(
        protocol_id="e00_instrument_qualification",
        domains=domains,
        items_per_domain=10,
        block_size=5,
        partition="engineering",
        seed=42,
    )

    assert plan.total_trials == 20
    assert plan.total_blocks == 4
    assert len(plan.blocks) == 4

    # Check block domain alternation (Block 1: geo, Block 2: logic, Block 3: geo, Block 4: logic)
    assert plan.blocks[0].domain == "world_geography"
    assert plan.blocks[0].item_count == 5
    assert plan.blocks[1].domain == "propositional_logic"
    assert plan.blocks[1].item_count == 5
    assert plan.blocks[2].domain == "world_geography"
    assert plan.blocks[2].item_count == 5
    assert plan.blocks[3].domain == "propositional_logic"
    assert plan.blocks[3].item_count == 5


def test_domain_session_scheduler_deterministic_reproducibility(session: Session):
    load_and_register_all_protocols(session)
    seed_qualification_items(session)

    scheduler = DomainSessionScheduler(session)
    domains = ["physical_science", "arithmetic"]

    plan1 = scheduler.plan_session("e00_instrument_qualification", domains, items_per_domain=6, block_size=3, seed=99)
    plan2 = scheduler.plan_session("e00_instrument_qualification", domains, items_per_domain=6, block_size=3, seed=99)

    item_ids_1 = [it.item_id for it in plan1.ordered_items]
    item_ids_2 = [it.item_id for it in plan2.ordered_items]

    assert item_ids_1 == item_ids_2
