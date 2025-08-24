from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models import Ticket, Surgery, FpaModification, db, TICKET_STATUS_VIGENTE, TICKET_STATUS_ANULADO
from sqlalchemy import func
from datetime import datetime, timedelta
import json

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
@login_required
def index():
    clinic_id = current_user.clinic_id
    now = datetime.now()
    start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    start_of_week = now - timedelta(days=now.weekday())
    start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
    
    overdue_tickets_count = Ticket.query.filter(
        Ticket.status == TICKET_STATUS_VIGENTE,
        Ticket.current_fpa < now,
        Ticket.clinic_id == clinic_id
    ).count()

    active_tickets_count = Ticket.query.filter(
        Ticket.status == TICKET_STATUS_VIGENTE,
        Ticket.current_fpa >= now,
        Ticket.clinic_id == clinic_id
    ).count()
    
    kpis = {
        'active_tickets': active_tickets_count,
        'annulled_tickets': Ticket.query.filter_by(status='Anulado', clinic_id=clinic_id).count(),
        'overdue_tickets': overdue_tickets_count,
        'total_tickets': Ticket.query.filter_by(clinic_id=clinic_id).count(),
        'monthly_tickets': Ticket.query.filter(Ticket.created_at >= start_of_month, Ticket.clinic_id == clinic_id).count(),
        'weekly_tickets': Ticket.query.filter(Ticket.created_at >= start_of_week, Ticket.clinic_id == clinic_id).count()
    }
    
    next_24h = now + timedelta(hours=24)
    near_deadline = Ticket.query.filter(
        Ticket.status == 'Vigente',
        Ticket.current_fpa <= next_24h,
        Ticket.current_fpa > now,
        Ticket.clinic_id == clinic_id
    ).count()
    
    kpis['near_deadline'] = near_deadline
    
    recent_tickets = Ticket.query.filter_by(clinic_id=clinic_id).order_by(Ticket.created_at.desc()).limit(8).all()
    
    surgery_stats = db.session.query(
        Surgery.name,
        func.count(Ticket.id).label('ticket_count')
    ).join(Ticket).filter(Ticket.clinic_id == clinic_id).group_by(Surgery.id, Surgery.name).order_by(func.count(Ticket.id).desc()).limit(5).all()
    
    weekly_trend = []
    for i in range(7):
        day = now - timedelta(days=6-i)
        day_start = day.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = day_start + timedelta(days=1)
        
        day_tickets = Ticket.query.filter(
            Ticket.created_at >= day_start,
            Ticket.created_at < day_end,
            Ticket.clinic_id == clinic_id
        ).count()
        
        weekly_trend.append({
            'date': day.strftime('%d/%m'),
            'tickets': day_tickets
        })
    
    total_modifications = FpaModification.query.filter_by(clinic_id=clinic_id).count()
    avg_modifications = round(total_modifications / kpis['total_tickets'] if kpis['total_tickets'] > 0 else 0, 1)
    
    tickets_with_mods = db.session.query(Ticket.id).join(FpaModification).filter(Ticket.clinic_id == clinic_id).distinct().count()
    
    modification_stats = {
        'total_modifications': total_modifications,
        'avg_modifications_per_ticket': avg_modifications,
        'tickets_with_modifications': tickets_with_mods
    }
    
    chart_data = {
        'weekly_trend': weekly_trend,
        'surgery_distribution': [{'surgery': s.name, 'count': s.ticket_count} for s in surgery_stats]
    }
    
    return render_template('dashboard.html', 
                         kpis=kpis, 
                         recent_tickets=recent_tickets,
                         surgery_stats=surgery_stats,
                         modification_stats=modification_stats,
                         chart_data=json.dumps(chart_data))