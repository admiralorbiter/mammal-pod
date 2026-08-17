"""Flask application factory for Project MAMMAL scientific instrument."""

from __future__ import annotations

from pathlib import Path

from flask import Flask

from mammal.config import Settings, settings
from mammal.db import init_db
from mammal.web.routes import routes


def create_app(app_settings: Settings | None = None) -> Flask:
    """Create and configure the Project MAMMAL Flask application."""
    target_settings = app_settings or settings
    target_settings.ensure_directories()

    template_dir = Path(__file__).parent / "web" / "templates"
    static_dir = Path(__file__).parent / "web" / "static"

    app = Flask(
        "mammal",
        template_folder=str(template_dir),
        static_folder=str(static_dir),
    )

    app.config["SETTINGS"] = target_settings
    app.config["SECRET_KEY"] = "project-mammal-local-instrument-key"

    # Initialize DB tables
    init_db(app_settings=target_settings)

    # Register routes
    app.register_blueprint(routes)

    return app


if __name__ == "__main__":
    flask_app = create_app()
    flask_app.run(host="127.0.0.1", port=5000, debug=True)
