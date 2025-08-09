import click
from flask.cli import with_appcontext
from models import db, User, Clinic, Surgery, Technique, StayAdjustmentCriterion, Doctor, DischargeTimeSlot, StandardizedReason, Patient, Ticket
from datetime import datetime, timedelta
import re

def generate_prefix(clinic_name):
    """Generates a short, unique prefix from a clinic name."""
    name_parts = clinic_name.replace("Clínica RedSalud", "").strip().lower()
    prefix = re.sub(r'[^a-z]', '', name_parts)[:4]
    return prefix

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Initialize the database with default data for all clinics."""
    db.create_all()
    
    if not Clinic.query.first():
        clinic_names = [
            "Clínica RedSalud Iquique", "Clínica RedSalud Elqui", "Clínica RedSalud Valparaíso",
            "Clínica RedSalud Providencia", "Clínica RedSalud Santiago", "Clínica RedSalud Vitacura",
            "Clínica RedSalud Rancagua", "Clínica RedSalud Mayor Temuco", "Clínica RedSalud Magallanes"
        ]
        for name in clinic_names:
            db.session.add(Clinic(name=name))
        db.session.commit()
        click.echo("Clinics populated.")
    
    all_clinics = Clinic.query.all()
    if not all_clinics:
        click.echo("No clinics found. Aborting data seeding.")
        return

    created_items = {}
    patient_rut_counter = 1

    for clinic in all_clinics:
        prefix = generate_prefix(clinic.name)
        click.echo(f"Populating data for {clinic.name} ({prefix})...")
        
        created_items[clinic.id] = {
            'surgeries': [], 'techniques': [], 'doctors': [], 'patients': []
        }

        # Create Users
        for role in ['admin', 'clinical', 'visualizador']:
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

        # Create Surgeries & Techniques
        surgeries_data = [
            {'name': 'Apendicectomía Laparoscópica', 'specialty': 'Cirugía General', 'is_ambulatory': False},
            {'name': 'Colecistectomía Laparoscópica', 'specialty': 'Cirugía General', 'is_ambulatory': True, 'ambulatory_cutoff_hour': 14},
        ]
        for s_data in surgeries_data:
            surgery = Surgery(
                name=f"{s_data['name']} ({prefix})", 
                specialty=s_data['specialty'], 
                is_ambulatory=s_data['is_ambulatory'], 
                ambulatory_cutoff_hour=s_data.get('ambulatory_cutoff_hour'), 
                clinic_id=clinic.id
            )
            db.session.add(surgery)
            db.session.flush()
            created_items[clinic.id]['surgeries'].append(surgery)
            
            tech = Technique(name=f'Técnica Estándar ({prefix})', base_stay_hours=24, surgery_id=surgery.id, clinic_id=clinic.id)
            db.session.add(tech)
            db.session.flush()
            created_items[clinic.id]['techniques'].append(tech)

        # Create Doctors
        doc = Doctor(name=f'Dr. Carlos Mendoza ({prefix})', specialty='Cirugía General', medical_license=f'12345-{prefix}', clinic_id=clinic.id)
        db.session.add(doc)
        db.session.flush()
        created_items[clinic.id]['doctors'].append(doc)

        # Create Patients
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

    db.session.commit()

    # Create Tickets
    ticket_counter = 1
    for clinic in all_clinics:
        prefix = generate_prefix(clinic.name)
        clinic_data = created_items[clinic.id]
        now = datetime.now()
        
        if clinic_data['patients'] and clinic_data['surgeries'] and clinic_data['techniques'] and clinic_data['doctors']:
            ticket1 = Ticket(
                id=f'TH-{prefix.upper()}-{now.year}-{ticket_counter:03d}',
                patient_id=clinic_data['patients'][0].id,
                surgery_id=clinic_data['surgeries'][0].id,
                technique_id=clinic_data['techniques'][0].id,
                doctor_id=clinic_data['doctors'][0].id,
                pavilion_end_time=now - timedelta(hours=10),
                initial_fpa=now + timedelta(hours=14),
                current_fpa=now + timedelta(hours=14),
                overnight_stays=1,
                created_by=f'admin_{prefix}',
                clinic_id=clinic.id
            )
            db.session.add(ticket1)
            ticket_counter += 1

    db.session.commit()
    click.echo("Database initialized with multi-clinic support and sample data.")

@click.command('reset-db')
@with_appcontext
def reset_db_command():
    """Drops all tables and re-initializes the database."""
    db.drop_all()
    init_db_command.callback()
    click.echo('Database has been reset.')

def register_commands(app):
    app.cli.add_command(init_db_command)
    app.cli.add_command(reset_db_command)
