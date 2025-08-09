from models import db, Ticket, Patient, Surgery
from datetime import datetime, timedelta
from flask_login import current_user

def _build_tickets_query(filters):
    """Builds a ticket query based on a dictionary of filters."""
    query = Ticket.query.join(Patient, Ticket.patient_id == Patient.id).join(Surgery, Ticket.surgery_id == Surgery.id).filter(
        Ticket.clinic_id == current_user.clinic_id,
        Patient.clinic_id == current_user.clinic_id,
        Surgery.clinic_id == current_user.clinic_id
    )

    if filters.get('status'):
        query = query.filter(Ticket.status == filters['status'])

    if filters.get('search'):
        search_query = filters['search']
        full_name_expr = db.func.concat(Patient.primer_nombre, ' ', Patient.apellido_paterno)
        if db.engine.dialect.name == 'sqlite':
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

    if filters.get('compliance'):
        query = query.filter(Ticket.compliance_status == filters['compliance'])

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