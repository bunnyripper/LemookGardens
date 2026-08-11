from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

db=SQLAlchemy()
migrate=Migrate()
login_manager=LoginManager()

limiter=Limiter(
    get_remote_address,
    default_limits=["200 per day","50 per hour"]
)

login_manager.login_view="admin.login"
login_manager.login_message="Please login to access this page."
login_manager.session_protection = 'strong'
@login_manager.user_loader
def load_user(user_id):
    from app.admin.routes import AdminUser
    return AdminUser(user_id)
