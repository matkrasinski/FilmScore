"""Main app file"""

from flask import Flask
from flask_cors import CORS

from .ai.views import ai_bp
from .config import db_status
from .database.model import *
from .database.util.import_pipeline import ImportPipeline
from .database.util.update_pipeline import UpdatePipeline
from .database.views import db_bp
from .extensions import db
from .config.scheduler import init_datetime_scheduler
import sys


def create_app(config_object="backend.settings"):
    app = Flask(import_name=__name__)
    app.config.from_object(obj=config_object)

    register_blueprints(app=app)
    init_cors(app=app)
    register_extensions(app=app)
    init_datetime_scheduler(UpdatePipeline().run_pipeline)
    init_options(app=app)

    return app


def register_blueprints(app):
    app.register_blueprint(blueprint=ai_bp)
    app.register_blueprint(blueprint=db_bp)


def init_options(app):
    dropDb = '--dropDb' in sys.argv
    updateData_index = sys.argv.index(
        '--updateData') if '--updateData' in sys.argv else None

    if dropDb:
        print('Dropping the database...')
        with app.app_context():
            db.drop_all()
    if updateData_index is not None and updateData_index + 1 < len(sys.argv):
        updateData = int(sys.argv[updateData_index + 1])
        with app.app_context():
            UpdatePipeline().run_pipeline(max_size=updateData)
        print(f'Updating data in the database with parameter: {updateData}')
    elif '--updateData' in sys.argv:
        with app.app_context():
            UpdatePipeline().run_pipeline()
        print('Updating all data in the database...')


def init_cors(app):
    CORS(app)


def register_extensions(app):
    db.init_app(app=app)


if __name__ == "__main__":
    main_app = create_app()

    with main_app.app_context():
        if not db_status.is_initialized():
            db.drop_all()
            db.create_all()
            ImportPipeline().run_pipeline()
            db_status.update_status()

    main_app.run(debug=False, host="0.0.0.0")
