from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from models import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('Por favor complete todos los campos.', 'error')
            return render_template('login.html')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.password == password and user.is_active:
            login_user(user)
            flash(f'¡Bienvenido, {user.username}!', 'success')
            if user.role == 'visualizador':
                return redirect(url_for('visualizador.dashboard'))
            return redirect(url_for('dashboard.index'))
        else:
            flash('Credenciales inválidas o usuario inactivo.', 'error')
    
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada exitosamente.', 'success')
    return redirect(url_for('auth.login'))