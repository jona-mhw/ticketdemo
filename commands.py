import click
from flask.cli import with_appcontext
from models import db, User, Clinic, Surgery, Technique, StayAdjustmentCriterion, Doctor, DischargeTimeSlot, StandardizedReason, Patient, Ticket
from datetime import datetime, timedelta
import re
import random

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

        # Create 2-hour Discharge Time Slots
        if not DischargeTimeSlot.query.filter_by(clinic_id=clinic.id).first():
            for i in range(0, 24, 2):
                start_time = datetime.strptime(f'{i:02d}:00', '%H:%M').time()
                
                end_hour = i + 2
                # The end of the day is 23:59:59
                if end_hour == 24:
                    end_time = datetime.strptime('23:59:59', '%H:%M:%S').time()
                    slot_name = f"{start_time.strftime('%H:%M')} - 00:00"
                else:
                    end_time = datetime.strptime(f'{end_hour:02d}:00', '%H:%M').time()
                    slot_name = f"{start_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')}"

                slot = DischargeTimeSlot(
                    name=slot_name,
                    start_time=start_time,
                    end_time=end_time,
                    clinic_id=clinic.id
                )
                db.session.add(slot)

        # Create Stay Adjustment Criteria
        criteria_data = [
            {'name': 'Comorbilidad Severa', 'hours_adjustment': 24, 'category': 'comorbidity'},
            {'name': 'Paciente Mayor de 80 años', 'hours_adjustment': 12, 'category': 'patient_factor'},
            {'name': 'Cirugía Previa Compleja', 'hours_adjustment': 8, 'category': 'surgical_history'},
        ]
        for c_data in criteria_data:
            criterion = StayAdjustmentCriterion(name=c_data['name'], hours_adjustment=c_data['hours_adjustment'], category=c_data['category'], clinic_id=clinic.id)
            db.session.add(criterion)

        # Create Standardized Reasons
        if not StandardizedReason.query.filter_by(clinic_id=clinic.id).first():
            reasons_data = [
                # Modification Reasons
                {'reason': 'Complicación post-operatoria', 'category': 'modification'},
                {'reason': 'Condición del paciente requiere más observación', 'category': 'modification'},
                {'reason': 'Resultados de laboratorio pendientes', 'category': 'modification'},
                {'reason': 'Solicitud del paciente/familia', 'category': 'modification'},
                # Annulment Reasons
                {'reason': 'Error en el ingreso de datos', 'category': 'annulment'},
                {'reason': 'Paciente transferido a otra unidad', 'category': 'annulment'},
                {'reason': 'Cirugía suspendida/reprogramada', 'category': 'annulment'},
                {'reason': 'Ticket duplicado', 'category': 'annulment'},
                # Non-Compliance Reasons (for closure)
                {'reason': 'Alta voluntaria', 'category': 'non_compliance'},
                {'reason': 'Transferencia a hospital de origen', 'category': 'non_compliance'},
                {'reason': 'Fuga del paciente', 'category': 'non_compliance'},
            ]
            for r_data in reasons_data:
                reason = StandardizedReason(
                    reason=r_data['reason'],
                    category=r_data['category'],
                    clinic_id=clinic.id
                )
                db.session.add(reason)

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

    # Create a variety of Tickets for testing
    click.echo("Creating sample tickets...")
    ticket_counter = 1
    for clinic in all_clinics:
        prefix = generate_prefix(clinic.name)
        clinic_data = created_items[clinic.id]
        
        if not all([clinic_data['patients'], clinic_data['surgeries'], clinic_data['techniques'], clinic_data['doctors']]):
            click.echo(f"Skipping ticket creation for {clinic.name} due to missing master data.")
            continue

        for i in range(15): # Create 15 tickets per clinic
            now = datetime.now()
            
            # Randomize data for variety
            patient = random.choice(clinic_data['patients'])
            surgery = random.choice(clinic_data['surgeries'])
            # Find a technique related to the chosen surgery
            technique = next((t for t in clinic_data['techniques'] if t.surgery_id == surgery.id), random.choice(clinic_data['techniques']))
            doctor = random.choice(clinic_data['doctors'])
            pavilion_end_time = now - timedelta(days=random.randint(0, 30), hours=random.randint(0, 23))
            
            # Base FPA calculation
            fpa, overnight_stays = Ticket().calculate_fpa(pavilion_end_time, technique.base_stay_hours, 0, surgery)

            ticket = Ticket(
                id=f'TH-{prefix.upper()}-{now.year}-{ticket_counter:03d}',
                patient_id=patient.id,
                surgery_id=surgery.id,
                technique_id=technique.id,
                doctor_id=doctor.id,
                pavilion_end_time=pavilion_end_time,
                initial_fpa=fpa,
                current_fpa=fpa,
                overnight_stays=overnight_stays,
                created_by=f'admin_{prefix}',
                clinic_id=clinic.id,
                status='Vigente'
            )
            
            # Randomly set some tickets to closed or annulled
            if i % 4 == 0:
                ticket.status = 'Cerrado'
                ticket.closed_at = pavilion_end_time + timedelta(days=overnight_stays, hours=random.randint(-5, 5))
                ticket.actual_discharge_date = ticket.closed_at
                ticket.compliance_status = 'compliant' if ticket.actual_discharge_date <= ticket.current_fpa else 'non_compliant'
            elif i % 7 == 0:
                ticket.status = 'Anulado'
                ticket.annulled_at = pavilion_end_time + timedelta(days=1)
                ticket.annulled_by = f'admin_{prefix}'
                ticket.annulled_reason = 'Error en el ingreso de datos'

            db.session.add(ticket)
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