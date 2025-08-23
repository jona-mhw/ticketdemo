from models import db, Ticket, Patient, Surgery, Doctor, ActionAudit
from datetime import datetime, timedelta
from flask_login import current_user
import re

def log_action(action, target_id=None, target_type=None):
    """Logs an action performed by the current user."""
    if not current_user.is_authenticated:
        return
    
    log_entry = ActionAudit(
        user_id=current_user.id,
        username=current_user.username,
        clinic_id=current_user.clinic_id,
        action=action,
        target_id=str(target_id) if target_id else None,
        target_type=target_type
    )
    db.session.add(log_entry)

def generate_prefix(clinic_name):
    """Generates a short, unique prefix from a clinic name."""
    name_parts = clinic_name.replace("Clínica RedSalud", "").strip().lower()
    prefix = re.sub(r'[^a-z]', '', name_parts)[:4]
    return prefix

def _build_tickets_query(filters):
    """Builds a ticket query based on a dictionary of filters."""
    query = Ticket.query.join(Patient, Ticket.patient_id == Patient.id).join(Surgery, Ticket.surgery_id == Surgery.id).outerjoin(Doctor, Ticket.doctor_id == Doctor.id).filter(
        Ticket.clinic_id == current_user.clinic_id,
        Patient.clinic_id == current_user.clinic_id,
        Surgery.clinic_id == current_user.clinic_id
    )

    if filters.get('status'):
        query = query.filter(Ticket.status == filters['status'])

    if filters.get('search'):
        search_query = filters['search']
        # In SQLite, CONCAT is not available, so we use the + operator.
        full_name_expr = Patient.primer_nombre + ' ' + Patient.apellido_paterno
        
        query = query.filter(
            db.or_(
                Ticket.id.contains(search_query),
                full_name_expr.contains(search_query),
                Patient.rut.contains(search_query)
            )
        )

    if filters.get('surgery'):
        query = query.filter(Surgery.id == int(filters['surgery']))

    if filters.get('date_from'):
        try:
            date_from_obj = datetime.strptime(filters['date_from'], '%Y-%m-%d')
            query = query.filter(Ticket.created_at >= date_from_obj)
        except (ValueError, TypeError):
            pass

    if filters.get('date_to'):
        try:
            date_to_obj = datetime.strptime(filters['date_to'], '%Y-%m-%d')
            date_to_obj += timedelta(days=1)
            query = query.filter(Ticket.created_at < date_to_obj)
        except (ValueError, TypeError):
            pass

    

    return query

def apply_sorting_to_query(query, sort_by, sort_dir):
    """Applies sorting to the ticket query."""
    order_logic = None
    
    if sort_by == 'patient':
        # Sort by paternal last name, maternal last name, then first name
        order_logic = [Patient.apellido_paterno, Patient.apellido_materno, Patient.primer_nombre]
    elif sort_by == 'surgery':
        order_logic = [Surgery.name]
    elif sort_by == 'doctor':
        order_logic = [Doctor.name]
    elif sort_by == 'fpa':
        order_logic = [Ticket.current_fpa]
    elif hasattr(Ticket, sort_by):
        order_logic = [getattr(Ticket, sort_by)]

    if order_logic:
        if sort_dir == 'desc':
            query = query.order_by(*[db.desc(c) for c in order_logic if c is not None])
        else:
            query = query.order_by(*[db.asc(c) for c in order_logic if c is not None])
    else:
        # Default sort
        query = query.order_by(db.desc(Ticket.created_at))
        
    return query

def calculate_time_remaining(fpa):
    """Calculate detailed time remaining until FPA."""
    if not fpa:
        return None
    
    now = datetime.now()
    if fpa <= now:
        return {'days': 0, 'hours': 0, 'minutes': 0, 'seconds': 0, 'expired': True}
    
    time_diff = fpa - now
    days = time_diff.days
    hours, remainder = divmod(time_diff.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    return {
        'days': days,
        'hours': hours,
        'minutes': minutes,
        'seconds': seconds,
        'expired': False
    }