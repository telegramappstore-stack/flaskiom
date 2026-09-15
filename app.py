from flask import Flask
from flask_login import user_loaded_from_request

from config import Config
from extensions import db, login_manager
from models import AdminUser


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        if user_id == app.config["ADMIN_USERNAME"]:
            return AdminUser(user_id)
        return None

    from blueprints.main import main_bp
    from blueprints.admin import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)

    with app.app_context():
        db.create_all()

    @app.context_processor
    def inject_globals():
        return {
            "site_name": app.config["SITE_NAME"],
            "site_currency": app.config["SITE_CURRENCY"],
        }

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
