from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    login_manager.login_view = 'admin.login'
    login_manager.login_message_category = 'info'

    from app.routes.main import main_bp
    from app.routes.admin import admin_bp
    from app.routes.blog import blog_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(blog_bp, url_prefix='/blog')

    @app.context_processor
    def inject_globals():
        from app.models import SiteSetting
        settings = {}
        for key in ['site_name', 'site_email', 'site_phone', 'site_address', 'site_hours']:
            settings[key] = SiteSetting.get(key)
        return dict(settings=settings)

    with app.app_context():
        from app import models
        db.create_all()

    return app
