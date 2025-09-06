from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from datetime import timedelta
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
migrate = Migrate()
jwt=JWTManager()
bcrypt = Bcrypt()
 
def create_app():
    app = Flask(__name__)

    
    # Load configuration from a config file or object
    app.config.from_object('config.Config')

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Register blueprints or routes here

    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(main_blueprint, url_prefix='/auth')
    #CROS SEETINGS OPEN FOR NOW ONLY
    CORS(app, resources={r"/*": {"origins": "*"}})


    return app


