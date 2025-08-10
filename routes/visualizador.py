from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from models import db, Ticket, Patient, Surgery
from datetime import datetime
from sqlalchemy import or_
from .utils import _build_tickets_query, calculate_time_remaining, apply_sorting_to_query

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

    query = apply_sorting_to_query(query, sort_by, sort_dir)

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