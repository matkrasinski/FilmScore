"""Main app file"""
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
from flask_cors import CORS
from waitress import serve

from .ai.views import ai_bp
from .config import db_status
from .database.model import *
from .database.util.import_pipeline import ImportPipeline
from .database.util.update_pipeline import UpdatePipeline
from .database.views import db_bp
from .extensions import db


def create_app(config_object="api.settings"):
    app = Flask(import_name=__name__)
    app.config.from_object(obj=config_object)

    register_blueprints(app=app)
    init_cors(app=app)
    register_extensions(app=app)
    init_daily_scheduler()

    return app


def register_blueprints(app):
    app.register_blueprint(blueprint=ai_bp)
    app.register_blueprint(blueprint=db_bp)


def init_cors(app):
    CORS(app)


def register_extensions(app):
    db.init_app(app=app)


def init_daily_scheduler(hour=2, minute=00, second=40):
    scheduler = BackgroundScheduler()
    daily_task = UpdatePipeline().run_pipeline
    scheduler.add_job(daily_task, "cron", hour=hour,
                      minute=minute, second=second)
    scheduler.start()


if __name__ == "__main__":
    main_app = create_app()
    data_pipeline = ImportPipeline()
    with main_app.app_context():
        if not db_status.is_initialized():
            db.drop_all()
            db.create_all()
            data_pipeline.run_pipeline()
            db_status.update_status()

    # serve(main_app, host="0.0.0.0", port=5000)
    main_app.run(debug=False)
