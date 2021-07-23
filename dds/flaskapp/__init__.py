from flaskapp.creds.db_uri import load_db_uri
import os
from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
session = Session()


def protect_dash(app):
    for view_func in app.server.view_functions:
        if view_func.startswith(app.config["url_base_pathname"]):
            app.server.view_functions[view_func] = login_required(
                app.server.view_functions[view_func]
            )


def init_app():
    server = Flask(__name__)
    # app.config.from_object('config.Config')
    server.config.update(
        DEBUG=True,
        DEVELOPMENT=True,
        TESTING=False,
        CSRF_ENABLED=True,
        SECRET_KEY=os.urandom(24),
        SQLALCHEMY_DATABASE_URI=load_db_uri(),
        SQLALCHEMY_TRACK_MODIFICATIONS=True,
        SESSION_TYPE="filesystem",
    )

    # Init Plugins
    db.init_app(server)
    migrate.init_app(server, db)
    login_manager.init_app(server)
    login_manager.login_view = "/login"
    session.init_app(server)

    # Register App Factory
    with server.app_context():
        from flaskapp.googleroutes import google_api
        from flaskapp.routes import routes_bp

        # Register Blueprints
        server.register_blueprint(google_api)
        server.register_blueprint(routes_bp)

        # Import Dash Application
        from dashapp.index import init_dashboard
        from homeapp.home_dash import init_home_dashboard

        app = init_dashboard(server)
        app2 = init_home_dashboard(server)

        # app = init_grade_dashboard(server)
        # app = init_inci_dashboard(server)
        # app = init_att_dashboard(server)

        protect_dash(app)
        protect_dash(app2)

        # Create DB Models
        db.create_all()

        return server
