from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models import db, User, Surgery, Technique, StayAdjustmentCriterion, StandardizedReason, Doctor, DischargeTimeSlot, Clinic, LoginAudit
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

@admin_bp.route('/clinics/<int:clinic_id>/toggle', methods=['POST'])
@login_required
@admin_required
def toggle_clinic(clinic_id):
    clinic = Clinic.query.get_or_404(clinic_id)
    try:
        clinic.is_active = not clinic.is_active
        db.session.commit()
        status = "activada" if clinic.is_active else "desactivada"
        flash(f'Clínica {clinic.name} {status} exitosamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al cambiar el estado de la clínica: {str(e)}', 'error')
    return redirect(url_for('admin.clinics'))

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
    
    if user.username == ROLE_ADMIN:
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

# Master Data Management
@admin_bp.route('/master-data/surgery', methods=['POST'])
@login_required
@admin_required
def create_surgery():
    try:
        name = request.form.get('name', '').strip()
        specialty = request.form.get('specialty', '').strip()
        if not name or not specialty:
            flash('Nombre y especialidad son obligatorios.', 'error')
        else:
            surgery = Surgery(name=name, specialty=specialty, clinic_id=current_user.clinic_id)
            db.session.add(surgery)
            db.session.commit()
            flash('Cirugía creada exitosamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al crear cirugía: {str(e)}', 'error')
    return redirect(url_for('admin.master_data'))

@admin_bp.route('/master-data/surgery/<int:surgery_id>/toggle', methods=['POST'])
@login_required
@admin_required
def toggle_surgery(surgery_id):
    surgery = Surgery.query.get_or_404(surgery_id)
    if surgery.clinic_id != current_user.clinic_id:
        flash('No tiene permisos para modificar esta cirugía.', 'error')
        return redirect(url_for('admin.master_data'))
    try:
        surgery.is_active = not surgery.is_active
        db.session.commit()
        status = "activada" if surgery.is_active else "desactivada"
        flash(f'Cirugía {surgery.name} {status} exitosamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al cambiar estado de la cirugía: {str(e)}', 'error')
    return redirect(url_for('admin.master_data'))

@admin_bp.route('/master-data/technique', methods=['POST'])
@login_required
@admin_required
def create_technique():
    try:
        name = request.form.get('name', '').strip()
        base_stay_hours = request.form.get('base_stay_hours', type=int)
        surgery_id = request.form.get('surgery_id', type=int)
        if not name or not base_stay_hours or not surgery_id:
            flash('Todos los campos son obligatorios.', 'error')
        else:
            technique = Technique(name=name, base_stay_hours=base_stay_hours, surgery_id=surgery_id, clinic_id=current_user.clinic_id)
            db.session.add(technique)
            db.session.commit()
            flash('Técnica creada exitosamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al crear técnica: {str(e)}', 'error')
    return redirect(url_for('admin.master_data'))

@admin_bp.route('/master-data/technique/<int:technique_id>/toggle', methods=['POST'])
@login_required
@admin_required
def toggle_technique(technique_id):
    technique = Technique.query.get_or_404(technique_id)
    if technique.clinic_id != current_user.clinic_id:
        flash('No tiene permisos para modificar esta técnica.', 'error')
        return redirect(url_for('admin.master_data'))
    try:
        technique.is_active = not technique.is_active
        db.session.commit()
        status = "activada" if technique.is_active else "desactivada"
        flash(f'Técnica {technique.name} {status} exitosamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al cambiar estado de la técnica: {str(e)}', 'error')
    return redirect(url_for('admin.master_data'))

@admin_bp.route('/master-data/adjustment', methods=['POST'])
@login_required
@admin_required
def create_adjustment():
    try:
        name = request.form.get('name', '').strip()
        hours_adjustment = request.form.get('hours_adjustment', type=int)
        category = request.form.get('category', '').strip()
        if not name or not hours_adjustment or not category:
            flash('Todos los campos son obligatorios.', 'error')
        else:
            adjustment = StayAdjustmentCriterion(name=name, hours_adjustment=hours_adjustment, category=category, clinic_id=current_user.clinic_id)
            db.session.add(adjustment)
            db.session.commit()
            flash('Criterio de ajuste creado exitosamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al crear criterio de ajuste: {str(e)}', 'error')
    return redirect(url_for('admin.master_data'))

@admin_bp.route('/master-data/adjustment/<int:adjustment_id>/toggle', methods=['POST'])
@login_required
@admin_required
def toggle_adjustment(adjustment_id):
    adjustment = StayAdjustmentCriterion.query.get_or_404(adjustment_id)
    if adjustment.clinic_id != current_user.clinic_id:
        flash('No tiene permisos para modificar este criterio.', 'error')
        return redirect(url_for('admin.master_data'))
    try:
        adjustment.is_active = not adjustment.is_active
        db.session.commit()
        status = "activado" if adjustment.is_active else "desactivado"
        flash(f'Criterio de ajuste {adjustment.name} {status} exitosamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al cambiar estado del criterio: {str(e)}', 'error')
    return redirect(url_for('admin.master_data'))

@admin_bp.route('/master-data/reason', methods=['POST'])
@login_required
@admin_required
def create_reason():
    try:
        reason = request.form.get('reason', '').strip()
        category = request.form.get('category', '').strip()
        if not reason or not category:
            flash('Razón y categoría son obligatorios.', 'error')
        else:
            standardized_reason = StandardizedReason(reason=reason, category=category, clinic_id=current_user.clinic_id)
            db.session.add(standardized_reason)
            db.session.commit()
            flash('Razón estandarizada creada exitosamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al crear razón estandarizada: {str(e)}', 'error')
    return redirect(url_for('admin.master_data'))

@admin_bp.route('/master-data/reason/<int:reason_id>/toggle', methods=['POST'])
@login_required
@admin_required
def toggle_reason(reason_id):
    reason = StandardizedReason.query.get_or_404(reason_id)
    if reason.clinic_id != current_user.clinic_id:
        flash('No tiene permisos para modificar esta razón.', 'error')
        return redirect(url_for('admin.master_data'))
    try:
        reason.is_active = not reason.is_active
        db.session.commit()
        status = "activada" if reason.is_active else "desactivada"
        flash(f'Razón estandarizada {status} exitosamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al cambiar estado de la razón: {str(e)}', 'error')
    return redirect(url_for('admin.master_data'))

@admin_bp.route('/master-data/doctor', methods=['POST'])
@login_required
@admin_required
def create_doctor():
    try:
        name = request.form.get('name', '').strip()
        specialty = request.form.get('specialty', '').strip()
        medical_license = request.form.get('medical_license', '').strip()
        if not name:
            flash('El nombre del médico es obligatorio.', 'error')
        else:
            doctor = Doctor(name=name, specialty=specialty, medical_license=medical_license, clinic_id=current_user.clinic_id)
            db.session.add(doctor)
            db.session.commit()
            flash('Médico creado exitosamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al crear médico: {str(e)}', 'error')
    return redirect(url_for('admin.master_data'))

@admin_bp.route('/master-data/doctor/<int:doctor_id>/toggle', methods=['POST'])
@login_required
@admin_required
def toggle_doctor(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    if doctor.clinic_id != current_user.clinic_id:
        flash('No tiene permisos para modificar este médico.', 'error')
        return redirect(url_for('admin.master_data'))
    try:
        doctor.is_active = not doctor.is_active
        db.session.commit()
        status = "activado" if doctor.is_active else "desactivado"
        flash(f'Médico {doctor.name} {status} exitosamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al cambiar estado del médico: {str(e)}', 'error')
    return redirect(url_for('admin.master_data'))


@admin_bp.route('/audit/logins')
@login_required
@admin_required
def login_audit():
    page = request.args.get('page', 1, type=int)
    logs = LoginAudit.query.filter_by(clinic_id=current_user.clinic_id).order_by(LoginAudit.timestamp.desc()).paginate(page=page, per_page=20)
    return render_template('admin/audit_log.html', logs=logs)


