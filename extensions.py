from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "admin.login"
login_manager.login_message = "برای دسترسی به این بخش باید وارد شوید."
login_manager.login_message_category = "warning"
