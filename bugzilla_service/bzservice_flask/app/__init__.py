import os
from flask import Flask
from .config import configure

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_oidc import OpenIDConnect
from flask_cors import CORS

from app.keycloak.keycloak_client import Keycloak
from app.bugzilla.bugzilla_client import BugzillaClient

db = SQLAlchemy()
ma = Marshmallow()
bcrypt = Bcrypt()
oidc = OpenIDConnect()

# Keycloak adapter
kc_client = Keycloak()
# Bugzilla adapter
bz_client = BugzillaClient()

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)
    configure("DEV", app)

    # serialize/deserialize
    ma = Marshmallow(app)

    with app.app_context():
        # Imports
        from .blueprints.auth.auth_bp import bp as auth_bp
        from .blueprints.products.products_bp import bp as products_bp
        from .blueprints.components.components_bp import bp as components_bp
        from .blueprints.bugs.bugs_bp import bp as bugs_bp
        from .blueprints.users.users_bp import bp as users_bp

        # DB connection configuration
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@bugzilladb:5432/bzsdb'
        #app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@10.50.80.3:5061/bzsdb'
        db.init_app(app)
        db.create_all()

        # flask-bcrypt
        bcrypt.init_app(app)

        # OpenIDConnect initialization
        oidc.init_app(app)

        app.register_blueprint(auth_bp)
        app.register_blueprint(products_bp)
        app.register_blueprint(components_bp)
        app.register_blueprint(bugs_bp)
        app.register_blueprint(users_bp)

        return app
