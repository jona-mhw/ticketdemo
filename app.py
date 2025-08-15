from flask import Flask, render_template, redirect, url_for, flash, request, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from dotenv import load_dotenv
from config import Config
from models import db, User
from commands import register_commands, seed_db
import os

load_dotenv()  # Carga las variables de entorno desde .env

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)

    # Database initialization is now handled by Flask commands.

    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor inicie sesión para acceder a esta página.'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Register blueprints
    from routes.auth import auth_bp
    from routes.dashboard import dashboard_bp
    from routes.tickets import tickets_bp
    from routes.admin import admin_bp
    from routes.visualizador import visualizador_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
    app.register_blueprint(tickets_bp, url_prefix='/tickets')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(visualizador_bp, url_prefix='/visualizador')
    
    # Root route
    @app.route('/')
    def index():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard.index'))
        return redirect(url_for('auth.login'))
    
    return app

app = create_app()
register_commands(app)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)