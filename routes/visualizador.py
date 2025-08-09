from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from models import db, Ticket, Patient, Surgery
from datetime import datetime
from sqlalchemy import or_
from routes.tickets import _build_tickets_query, calculate_time_remaining

visualizador_bp = Blueprint('visualizador', __name__, url_prefix='/visualizador')

@visualizador_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role not in ['admin', 'visualizador']:
        return "Acceso no autorizado", 403

    filters = {
        'status': request.args.get('status', ''),
        'search': request.args.get('search', ''),
        'surgery': request.args.get('surgery', ''),
        'date_from': request.args.get('date_from', ''),
        'date_to': request.args.get('date_to', ''),
        'compliance': request.args.get('compliance', '')
    }
    sort_by = request.args.get('sort_by', 'created_at')
    sort_dir = request.args.get('sort_dir', 'desc')

    query = _build_tickets_query(filters)

    if sort_by == 'patient':
        order_column = Patient.primer_nombre
    elif sort_by == 'surgery':
        order_column = Surgery.name
    elif sort_by == 'fpa':
        order_column = Ticket.current_fpa
    else:
        order_column = getattr(Ticket, sort_by, Ticket.created_at)

    if sort_dir == 'desc':
        query = query.order_by(db.desc(order_column))
    else:
        query = query.order_by(db.asc(order_column))

    tickets = query.all()
    tickets_fpa_count = query.filter(Ticket.current_fpa.isnot(None)).count()

    for ticket in tickets:
        if ticket.status == 'Vigente' and ticket.current_fpa:
            ticket.time_remaining = calculate_time_remaining(ticket.current_fpa)
        else:
            ticket.time_remaining = None

    surgeries = Surgery.query.filter_by(is_active=True, clinic_id=current_user.clinic_id).all()

    return render_template(
        'visualizador/dashboard.html',
        tickets=tickets,
        tickets_fpa_count=tickets_fpa_count,
        surgeries=surgeries,
        filters=filters
    )