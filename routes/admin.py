from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models import db, User, Surgery, Technique, StayAdjustmentCriterion, StandardizedReason, Doctor, DischargeTimeSlot, Clinic
from functools import wraps
from datetime import datetime, time

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin():
            flash('Acceso denegado. Se requieren permisos de administrador.', 'error')
            return redirect(url_for('dashboard.index'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/')
@login_required
@admin_required
def index():
    stats = {
        'users': User.query.filter_by(is_active=True, clinic_id=current_user.clinic_id).count(),
        'doctors': Doctor.query.filter_by(is_active=True, clinic_id=current_user.clinic_id).count(),
        'surgeries': Surgery.query.filter_by(is_active=True, clinic_id=current_user.clinic_id).count(),
        'techniques': Technique.query.filter_by(is_active=True, clinic_id=current_user.clinic_id).count(),
        'criteria': StayAdjustmentCriterion.query.filter_by(is_active=True, clinic_id=current_user.clinic_id).count(),
        'time_slots': DischargeTimeSlot.query.filter_by(is_active=True, clinic_id=current_user.clinic_id).count(),
        'reasons': StandardizedReason.query.filter_by(is_active=True, clinic_id=current_user.clinic_id).count(),
        'clinics': Clinic.query.filter_by(is_active=True).count(),
    }
    return render_template('admin/index.html', stats=stats)

# Clinic Management
@admin_bp.route('/clinics')
@login_required
@admin_required
def clinics():
    clinics = Clinic.query.all()
    return render_template('admin/clinics.html', clinics=clinics)

@admin_bp.route('/clinics/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_clinic():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        if not name:
            flash('El nombre de la clínica es obligatorio.', 'error')
        elif Clinic.query.filter_by(name=name).first():
            flash('Ya existe una clínica con ese nombre.', 'error')
        else:
            try:
                clinic = Clinic(name=name)
                db.session.add(clinic)
                db.session.commit()
                flash(f'Clínica {name} creada exitosamente.', 'success')
                return redirect(url_for('admin.clinics'))
            except Exception as e:
                db.session.rollback()
                flash(f'Error al crear la clínica: {str(e)}', 'error')
    return render_template('admin/clinic_form.html', clinic=None)

@admin_bp.route('/clinics/<int:clinic_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_clinic(clinic_id):
    clinic = Clinic.query.get_or_404(clinic_id)
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        is_active = request.form.get('is_active') == 'on'
        if not name:
            flash('El nombre de la clínica es obligatorio.', 'error')
        else:
            try:
                clinic.name = name
                clinic.is_active = is_active
                db.session.commit()
                flash(f'Clínica {name} actualizada exitosamente.', 'success')
                return redirect(url_for('admin.clinics'))
            except Exception as e:
                db.session.rollback()
                flash(f'Error al actualizar la clínica: {str(e)}', 'error')
    return render_template('admin/clinic_form.html', clinic=clinic)

@admin_bp.route('/users')
@login_required
@admin_required
def users():
    users = User.query.filter_by(clinic_id=current_user.clinic_id).all()
    clinics = Clinic.query.filter_by(is_active=True).all()
    return render_template('admin/users.html', users=users, clinics=clinics)

@admin_bp.route('/users/create', methods=['POST'])
@login_required
@admin_required
def create_user():
    try:
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        role = request.form.get('role', 'clinical')
        clinic_id = request.form.get('clinic_id', type=int)
        
        if not all([username, email, password, clinic_id]):
            flash('Todos los campos son obligatorios.', 'error')
            return redirect(url_for('admin.users'))
        
        if User.query.filter_by(username=username).first():
            flash('El nombre de usuario ya existe.', 'error')
            return redirect(url_for('admin.users'))
        
        if User.query.filter_by(email=email).first():
            flash('El email ya está registrado.', 'error')
            return redirect(url_for('admin.users'))
        
        user = User(username=username, email=email, role=role, clinic_id=clinic_id)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        flash(f'Usuario {username} creado exitosamente.', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error al crear usuario: {str(e)}', 'error')
    
    return redirect(url_for('admin.users'))

@admin_bp.route('/users/<int:user_id>/toggle', methods=['POST'])
@login_required
@admin_required
def toggle_user(user_id):
    user = User.query.filter_by(id=user_id, clinic_id=current_user.clinic_id).first_or_404()
    
    if user.username == 'admin':
        flash('No se puede desactivar el usuario administrador principal.', 'error')
        return redirect(url_for('admin.users'))
    
    try:
        user.is_active = not user.is_active
        db.session.commit()
        
        status = "activado" if user.is_active else "desactivado"
        flash(f'Usuario {user.username} {status} exitosamente.', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error al cambiar estado del usuario: {str(e)}', 'error')
    
    return redirect(url_for('admin.users'))

@admin_bp.route('/master-data')
@login_required
@admin_required
def master_data():
    clinic_id = current_user.clinic_id
    surgeries = Surgery.query.filter_by(clinic_id=clinic_id).all()
    techniques = Technique.query.filter_by(clinic_id=clinic_id).all()
    adjustments = StayAdjustmentCriterion.query.filter_by(clinic_id=clinic_id).all()
    reasons = StandardizedReason.query.filter_by(clinic_id=clinic_id).all()
    doctors = Doctor.query.filter_by(clinic_id=clinic_id).all()
    
    return render_template('admin/master_data.html', 
                         surgeries=surgeries, 
                         techniques=techniques,
                         adjustments=adjustments,
                         reasons=reasons,
                         doctors=doctors)

# ... (The rest of the routes remain the same)
