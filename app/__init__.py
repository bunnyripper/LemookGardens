from flask import Flask
from .extensions import db,migrate,login_manager,limiter



def create_app():
    app=Flask(__name__)
    app.config.from_object("config.Config")
    
    db.init_app(app)
    migrate.init_app(app,db)
    login_manager.init_app(app)
    
    limiter.init_app(app)
    
    from app import models
    
    
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    from app.admin import bp as admin_bp
    app.register_blueprint(admin_bp,url_prefix="/admin")
    
    return app