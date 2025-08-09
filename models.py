from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import json

db = SQLAlchemy()

class Clinic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    is_active = db.Column(db.Boolean, default=True)

    # Relationships
    users = db.relationship('User', backref='clinic', lazy=True)
    surgeries = db.relationship('Surgery', backref='clinic', lazy=True)
    techniques = db.relationship('Technique', backref='clinic', lazy=True)
    stay_adjustment_criteria = db.relationship('StayAdjustmentCriterion', backref='clinic', lazy=True)
    doctors = db.relationship('Doctor', backref='clinic', lazy=True)
    discharge_time_slots = db.relationship('DischargeTimeSlot', backref='clinic', lazy=True)
    standardized_reasons = db.relationship('StandardizedReason', backref='clinic', lazy=True)
    patients = db.relationship('Patient', backref='clinic', lazy=True)
    tickets = db.relationship('Ticket', backref='clinic', lazy=True)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='clinical')  # 'admin', 'clinical' or 'visualizador'
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    clinic_id = db.Column(db.Integer, db.ForeignKey('clinic.id'), nullable=False)
    
    def set_password(self, password):
        self.password = password
    
    def check_password(self, password):
        return self.password == password
    
    def is_admin(self):
        return self.role == 'admin'

class Surgery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    specialty = db.Column(db.String(100), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    applies_ticket_home = db.Column(db.Boolean, default=True)
    is_ambulatory = db.Column(db.Boolean, default=False)
    ambulatory_cutoff_hour = db.Column(db.Integer, nullable=True)
    clinic_id = db.Column(db.Integer, db.ForeignKey('clinic.id'), nullable=False)
    
    techniques = db.relationship('Technique', backref='surgery', lazy=True)

class Technique(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    base_stay_hours = db.Column(db.Integer, nullable=False)
    surgery_id = db.Column(db.Integer, db.ForeignKey('surgery.id'), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    clinic_id = db.Column(db.Integer, db.ForeignKey('clinic.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'base_stay_hours': self.base_stay_hours,
            'surgery_id': self.surgery_id
        }

class StayAdjustmentCriterion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    hours_adjustment = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    clinic_id = db.Column(db.Integer, db.ForeignKey('clinic.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'hours_adjustment': self.hours_adjustment,
            'category': self.category
        }

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    specialty = db.Column(db.String(100), nullable=True)
    medical_license = db.Column(db.String(50), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    clinic_id = db.Column(db.Integer, db.ForeignKey('clinic.id'), nullable=False)
    
    tickets = db.relationship('Ticket', backref='attending_doctor', lazy=True)

class DischargeTimeSlot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    clinic_id = db.Column(db.Integer, db.ForeignKey('clinic.id'), nullable=False)
    
    tickets = db.relationship('Ticket', backref='discharge_time_slot', lazy=True)

class StandardizedReason(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reason = db.Column(db.String(500), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    clinic_id = db.Column(db.Integer, db.ForeignKey('clinic.id'), nullable=False)

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rut = db.Column(db.String(12), nullable=False, index=True)
    primer_nombre = db.Column(db.String(100), nullable=False)
    segundo_nombre = db.Column(db.String(100), nullable=True)
    apellido_paterno = db.Column(db.String(100), nullable=False)
    apellido_materno = db.Column(db.String(100), nullable=True)
    age = db.Column(db.Integer, nullable=False)
    sex = db.Column(db.String(10), nullable=False)
    episode_id = db.Column(db.String(50), nullable=True)
    room_location = db.Column(db.String(100), nullable=True)
    clinic_id = db.Column(db.Integer, db.ForeignKey('clinic.id'), nullable=False)
    
    tickets = db.relationship('Ticket', backref='patient', lazy=True)

    @property
    def full_name(self):
        parts = [self.primer_nombre, self.segundo_nombre, self.apellido_paterno, self.apellido_materno]
        return ' '.join(part for part in parts if part)

class Ticket(db.Model):
    id = db.Column(db.String(20), primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=True)
    surgery_id = db.Column(db.Integer, db.ForeignKey('surgery.id'), nullable=True)
    technique_id = db.Column(db.Integer, db.ForeignKey('technique.id'), nullable=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=True)
    discharge_slot_id = db.Column(db.Integer, db.ForeignKey('discharge_time_slot.id'), nullable=True)
    clinic_id = db.Column(db.Integer, db.ForeignKey('clinic.id'), nullable=False)
    
    stay_adjustment_ids = db.Column(db.Text, nullable=True)
    
    pavilion_end_time = db.Column(db.DateTime, nullable=False)
    initial_fpa = db.Column(db.DateTime, nullable=False)
    current_fpa = db.Column(db.DateTime, nullable=False)
    overnight_stays = db.Column(db.Integer, nullable=False)
    
    status = db.Column(db.String(20), nullable=False, default='Vigente')
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.String(80), nullable=False)
    
    closed_at = db.Column(db.DateTime, nullable=True)
    closed_reason = db.Column(db.String(500), nullable=True)
    actual_discharge_date = db.Column(db.DateTime, nullable=True)
    compliance_status = db.Column(db.String(20), nullable=True)
    
    annulled_at = db.Column(db.DateTime, nullable=True)
    annulled_reason = db.Column(db.String(500), nullable=True)
    annulled_by = db.Column(db.String(80), nullable=True)
    
    surgery = db.relationship('Surgery', backref='tickets')
    technique = db.relationship('Technique', backref='tickets')
    modifications = db.relationship('FpaModification', backref='ticket', lazy=True, cascade='all, delete-orphan')
    
    def get_stay_adjustment_ids(self):
        if self.stay_adjustment_ids:
            return json.loads(self.stay_adjustment_ids)
        return []
    
    def set_stay_adjustment_ids(self, ids):
        self.stay_adjustment_ids = json.dumps(ids)
    
    def calculate_fpa(self, pavilion_end_time, base_hours, adjustment_hours=0, surgery=None):
        total_hours = base_hours + adjustment_hours
        fpa = pavilion_end_time + timedelta(hours=total_hours)
        
        if surgery and surgery.is_ambulatory and surgery.ambulatory_cutoff_hour:
            pavilion_hour = pavilion_end_time.hour
            cutoff_hour = surgery.ambulatory_cutoff_hour
            
            if pavilion_hour < cutoff_hour:
                next_morning = pavilion_end_time.replace(hour=8, minute=0, second=0, microsecond=0) + timedelta(days=1)
                if fpa < next_morning:
                    fpa = next_morning
        
        time_diff = fpa - pavilion_end_time
        overnight_stays = max(0, time_diff.days)
        if time_diff.seconds > 0:
            overnight_stays += 1
            
        return fpa, overnight_stays
    
    def can_be_modified(self):
        return self.status == 'Vigente'
    
    def get_modification_count(self):
        return len(self.modifications)

class FpaModification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.String(20), db.ForeignKey('ticket.id'), nullable=False)
    clinic_id = db.Column(db.Integer, db.ForeignKey('clinic.id'), nullable=False)
    
    previous_fpa = db.Column(db.DateTime, nullable=False)
    new_fpa = db.Column(db.DateTime, nullable=False)
    reason = db.Column(db.String(500), nullable=False)
    justification = db.Column(db.Text, nullable=True)
    
    modified_at = db.Column(db.DateTime, default=datetime.utcnow)
    modified_by = db.Column(db.String(80), nullable=False)

