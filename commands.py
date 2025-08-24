import click
import json
from flask.cli import with_appcontext
from sqlalchemy import text
from models import (
    db, User, Clinic, Surgery, Specialty, StayAdjustmentCriterion, Doctor, 
    DischargeTimeSlot, StandardizedReason, Patient, Ticket,
    ROLE_ADMIN, ROLE_CLINICAL, ROLE_VISUALIZADOR,
    TICKET_STATUS_VIGENTE, TICKET_STATUS_ANULADO,
    REASON_CATEGORY_MODIFICATION, REASON_CATEGORY_ANNULMENT
)
from datetime import datetime, timedelta
import random
import os
from flask import current_app
from routes.utils import generate_prefix

# --- Seeding Helper Functions ---

def _seed_clinics(is_production):
    """Seeds the clinics based on the environment."""
    if Clinic.query.first():
        return

    if is_production:
        clinic_names = ["Clínica RedSalud Providencia", "Clínica RedSalud Santiago"]
        print("Production environment detected. Populating with minimal clinics...")
    else:
        clinic_names = [
            "Clínica RedSalud Iquique", "Clínica RedSalud Elqui", "Clínica RedSalud Valparaíso",
            "Clínica RedSalud Providencia", "Clínica RedSalud Santiago", "Clínica RedSalud Vitacura",
            "Clínica RedSalud Rancagua", "Clínica RedSalud Mayor Temuco", "Clínica RedSalud Magallanes"
        ]
        print("Development environment. Populating with all clinics...")
    
    for name in clinic_names:
        db.session.add(Clinic(name=name))
    db.session.commit()
    print(f"{len(clinic_names)} clinics populated.")

def _seed_users_for_clinic(clinic, prefix):
    """Seeds the users for a specific clinic."""
    for role in [ROLE_ADMIN, ROLE_CLINICAL, ROLE_VISUALIZADOR]:
        username = f'{role}_{prefix}'
        if not User.query.filter_by(username=username).first():
            user = User(
                username=username,
                email=f'{username}@tickethome.com',
                role=role,
                password='password123',
                clinic_id=clinic.id
            )
            db.session.add(user)

def _seed_master_data_for_clinic(clinic, prefix, created_items):
    """Seeds all master data (specialties, surgeries, doctors, etc.) for a clinic."""
    # Specialties
    specialties_data = ['Cirugía General', 'Ginecología', 'Traumatología', 'Cirugía Pediátrica']
    for spec_name in specialties_data:
        specialty = Specialty(name=f"{spec_name} ({prefix})", clinic_id=clinic.id)
        db.session.add(specialty)
        db.session.flush()
        created_items[clinic.id]['specialties'].append(specialty)

    # Surgeries
    surgeries_data = [
        {'name': 'Apendicectomía Laparoscópica', 'specialty_name': 'Cirugía General', 'base_stay_hours': 24, 'is_ambulatory': False},
        {'name': 'Colecistectomía Laparoscópica', 'specialty_name': 'Cirugía General', 'base_stay_hours': 48, 'is_ambulatory': True, 'ambulatory_cutoff_hour': 14},
        {'name': 'Histerectomía Abdominal', 'specialty_name': 'Ginecología', 'base_stay_hours': 72, 'is_ambulatory': False},
        {'name': 'Artroscopia de Rodilla', 'specialty_name': 'Traumatología', 'base_stay_hours': 8, 'is_ambulatory': True, 'ambulatory_cutoff_hour': 16},
    ]
    for s_data in surgeries_data:
        # Find the specialty created for this clinic
        specialty = next((s for s in created_items[clinic.id]['specialties'] if s.name.startswith(s_data['specialty_name'])), None)
        if not specialty:
            continue

        surgery = Surgery(
            name=f"{s_data['name']} ({prefix})", 
            specialty_id=specialty.id,
            base_stay_hours=s_data['base_stay_hours'],
            is_ambulatory=s_data['is_ambulatory'], 
            ambulatory_cutoff_hour=s_data.get('ambulatory_cutoff_hour'), 
            clinic_id=clinic.id
        )
        db.session.add(surgery)
        db.session.flush()
        created_items[clinic.id]['surgeries'].append(surgery)

    # Doctors
    doctors_data = [
        {'name': 'Dr. Carlos Mendoza', 'specialty': 'Cirugía General', 'license': '12345'},
        {'name': 'Dra. Ana María Pérez', 'specialty': 'Ginecología', 'license': '54321'},
        {'name': 'Dr. Juan Pablo Soto', 'specialty': 'Traumatología', 'license': '67890'},
        {'name': 'Dra. Carolina Rojas', 'specialty': 'Cirugía Pediátrica', 'license': '09876'}
    ]
    for doc_data in doctors_data:
        doc = Doctor(
            name=f"{doc_data['name']} ({prefix})",
            specialty=doc_data['specialty'],
            medical_license=f"{doc_data['license']}-{prefix}",
            clinic_id=clinic.id
        )
        db.session.add(doc)
        db.session.flush()
        created_items[clinic.id]['doctors'].append(doc)

    # Discharge Time Slots
    if not DischargeTimeSlot.query.filter_by(clinic_id=clinic.id).first():
        for i in range(0, 24, 2):
            start_time = datetime.strptime(f'{i:02d}:00', '%H:%M').time()
            end_hour = i + 2
            end_time_str = f'{end_hour:02d}:00' if end_hour < 24 else '23:59:59'
            end_time = datetime.strptime(end_time_str, '%H:%M:%S' if end_hour == 24 else '%H:%M').time()
            slot_name = f"{start_time.strftime('%H:%M')} - {'00:00' if end_hour == 24 else end_time.strftime('%H:%M')}"
            slot = DischargeTimeSlot(name=slot_name, start_time=start_time, end_time=end_time, clinic_id=clinic.id)
            db.session.add(slot)

    # Stay Adjustment Criteria
    if not StayAdjustmentCriterion.query.filter_by(clinic_id=clinic.id).first():
        criteria_data = [
            {'name': 'Comorbilidad Severa', 'hours_adjustment': 24, 'category': 'comorbidity'},
            {'name': 'Paciente Mayor de 80 años', 'hours_adjustment': 12, 'category': 'patient_factor'},
            {'name': 'Cirugía Previa Compleja', 'hours_adjustment': 8, 'category': 'surgical_history'},
        ]
        for c_data in criteria_data:
            criterion = StayAdjustmentCriterion(name=c_data['name'], hours_adjustment=c_data['hours_adjustment'], category=c_data['category'], clinic_id=clinic.id)
            db.session.add(criterion)

    # Standardized Reasons
    if not StandardizedReason.query.filter_by(clinic_id=clinic.id).first():
        reasons_data = [
            {'reason': 'Complicación post-operatoria', 'category': REASON_CATEGORY_MODIFICATION},
            {'reason': 'Condición del paciente requiere más observación', 'category': REASON_CATEGORY_MODIFICATION},
            {'reason': 'Resultados de laboratorio pendientes', 'category': REASON_CATEGORY_MODIFICATION},
            {'reason': 'Solicitud del paciente/familia', 'category': REASON_CATEGORY_MODIFICATION},
            {'reason': 'Error en el ingreso de datos', 'category': REASON_CATEGORY_ANNULMENT},
            {'reason': 'Paciente transferido a otra unidad', 'category': REASON_CATEGORY_ANNULMENT},
            {'reason': 'Cirugía suspendida/reprogramada', 'category': REASON_CATEGORY_ANNULMENT},
            {'reason': 'Ticket duplicado', 'category': REASON_CATEGORY_ANNULMENT},
        ]
        for r_data in reasons_data:
            reason = StandardizedReason(reason=r_data['reason'], category=r_data['category'], clinic_id=clinic.id)
            db.session.add(reason)

def _seed_patients_for_clinic(clinic, prefix, created_items, patient_rut_counter):
    """Seeds dummy patients for a clinic."""
    for i in range(2):
        rut = f'{patient_rut_counter:08d}-K'
        patient = Patient(
            rut=rut, 
            primer_nombre=f'Paciente {i+1} ({prefix})', 
            apellido_paterno='Demo', 
            age=40 + i, 
            sex='Masculino', 
            clinic_id=clinic.id
        )
        db.session.add(patient)
        db.session.flush()
        created_items[clinic.id]['patients'].append(patient)
        patient_rut_counter += 1
    return patient_rut_counter

def _seed_tickets_for_clinic(clinic, prefix, created_items, is_production):
    """Seeds sample tickets for a clinic."""
    num_tickets = 2 if is_production else 15
    clinic_data = created_items[clinic.id]
    
    if not all([clinic_data['patients'], clinic_data['surgeries'], clinic_data['doctors']]):
        print(f"Skipping ticket creation for {clinic.name} due to missing master data.")
        return

    # Get all adjustment criteria for the clinic once
    all_adjustments = StayAdjustmentCriterion.query.filter_by(clinic_id=clinic.id).all()

    for i in range(num_tickets):
        now = datetime.now()
        patient = random.choice(clinic_data['patients'])
        surgery = random.choice(clinic_data['surgeries'])
        doctor = random.choice(clinic_data['doctors'])
        pavilion_end_time = now - timedelta(days=random.randint(0, 30), hours=random.randint(0, 23))
        
        # Simulate selecting some random adjustment criteria
        num_adjustments_to_pick = random.randint(0, len(all_adjustments))
        selected_adjustments = random.sample(all_adjustments, num_adjustments_to_pick)
        adjustment_hours = sum(adj.hours_adjustment for adj in selected_adjustments)
        adjustment_ids = [adj.id for adj in selected_adjustments]

        fpa, overnight_stays = Ticket().calculate_fpa(pavilion_end_time, surgery, adjustment_hours)

        ticket = Ticket(
            id=f'TH-{prefix.upper()}-{now.year}-{i+1:03d}',
            patient_id=patient.id,
            surgery_id=surgery.id,
            doctor_id=doctor.id,
            pavilion_end_time=pavilion_end_time,
            initial_fpa=fpa,
            current_fpa=fpa,
            overnight_stays=overnight_stays,
            created_by=f'{ROLE_ADMIN}_{prefix}',
            clinic_id=clinic.id,
            status=TICKET_STATUS_VIGENTE,
            # Populate snapshot fields
            surgery_name_snapshot=surgery.name,
            surgery_base_hours_snapshot=surgery.base_stay_hours,
            adjustment_criteria_snapshot=json.dumps([
                {'id': adj.id, 'name': adj.name, 'hours_adjustment': adj.hours_adjustment} for adj in selected_adjustments
            ])
        )
        ticket.set_stay_adjustment_ids(adjustment_ids)
        
        if i % 7 == 0:
            ticket.status = TICKET_STATUS_ANULADO
            ticket.annulled_at = pavilion_end_time + timedelta(days=1)
            ticket.annulled_by = f'{ROLE_ADMIN}_{prefix}'
            ticket.annulled_reason = 'Error en el ingreso de datos'

        db.session.add(ticket)

# --- Main Seeding Function ---

def seed_db():
    """Orchestrates the database seeding process."""
    is_production = os.environ.get('K_SERVICE') is not None
    _seed_clinics(is_production)
    
    all_clinics = Clinic.query.all()
    if not all_clinics:
        print("No clinics found. Aborting data seeding.")
        return

    created_items = {}
    patient_rut_counter = 1

    for clinic in all_clinics:
        prefix = generate_prefix(clinic.name)
        print(f"Populating data for {clinic.name} ({prefix})...")
        
        created_items[clinic.id] = {'specialties': [], 'surgeries': [], 'doctors': [], 'patients': []}
        
        _seed_users_for_clinic(clinic, prefix)
        _seed_master_data_for_clinic(clinic, prefix, created_items)
        patient_rut_counter = _seed_patients_for_clinic(clinic, prefix, created_items, patient_rut_counter)

    db.session.commit() # Commit users, master data, and patients before creating tickets

    print("Creating sample tickets...")
    for clinic in all_clinics:
        prefix = generate_prefix(clinic.name)
        _seed_tickets_for_clinic(clinic, prefix, created_items, is_production)

    db.session.commit()
    print("Database seeding complete.")

# --- Click Commands ---

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Initialize the database with default data for all clinics."""
    db.create_all()
    seed_db()
    click.echo("Database initialized with multi-clinic support and sample data.")

@click.command('reset-db')
@with_appcontext
def reset_db_command():
    """Drops all tables and re-initializes the database."""
    # Use raw SQL to drop and recreate the public schema for a clean slate
    with db.engine.connect() as con:
        # The DB user must have permissions to drop and create schemas.
        # In Supabase, the default 'postgres' user has this permission.
        click.echo('Wiping database schema (DROP SCHEMA public CASCADE)...')
        con.execute(text('DROP SCHEMA public CASCADE;'))
        con.execute(text('CREATE SCHEMA public;'))
        con.commit()
    
    click.echo('Database schema wiped and recreated.')
    
    # Now create tables based on current models
    db.create_all()
    click.echo('Database tables created.')
    
    # Seed the database with fresh data
    seed_db()
    click.echo('Database has been reset and seeded.')

def register_commands(app):
    app.cli.add_command(init_db_command)
    app.cli.add_command(reset_db_command)
