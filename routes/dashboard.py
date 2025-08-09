from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models import Ticket, Surgery, FpaModification, db
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
    
    kpis = {
        'active_tickets': Ticket.query.filter_by(status='Vigente', clinic_id=clinic_id).count(),
        'closed_tickets': Ticket.query.filter_by(status='Cerrado', clinic_id=clinic_id).count(),
        'annulled_tickets': Ticket.query.filter_by(status='Anulado', clinic_id=clinic_id).count(),
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
    
    overdue_tickets = Ticket.query.filter(
        Ticket.status == 'Vigente',
        Ticket.current_fpa < now,
        Ticket.clinic_id == clinic_id
    ).count()
    
    kpis['near_deadline'] = near_deadline
    kpis['overdue_tickets'] = overdue_tickets
    
    recent_tickets = Ticket.query.filter_by(clinic_id=clinic_id).order_by(Ticket.created_at.desc()).limit(8).all()
    
    closed_tickets = Ticket.query.filter_by(status='Cerrado', clinic_id=clinic_id).all()
    compliant_count = 0
    non_compliant_count = 0
    total_stay_hours = 0
    
    for ticket in closed_tickets:
        if ticket.compliance_status == 'compliant':
            compliant_count += 1
        elif ticket.compliance_status == 'non_compliant':
            non_compliant_count += 1
        
        if ticket.actual_discharge_date and ticket.pavilion_end_time:
            stay_duration = ticket.actual_discharge_date - ticket.pavilion_end_time
            total_stay_hours += stay_duration.total_seconds() / 3600
    
    total_closed = len(closed_tickets)
    compliance_stats = {
        'compliant_count': compliant_count,
        'non_compliant_count': non_compliant_count,
        'total_closed': total_closed,
        'compliant_percentage': round((compliant_count / total_closed * 100) if total_closed > 0 else 0, 1),
        'non_compliant_percentage': round((non_compliant_count / total_closed * 100) if total_closed > 0 else 0, 1),
        'average_stay_hours': round(total_stay_hours / total_closed if total_closed > 0 else 0, 1),
        'average_stay_days': round((total_stay_hours / total_closed / 24) if total_closed > 0 else 0, 1)
    }
    
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
    
    monthly_compliance = []
    for i in range(6):
        month_start = (now.replace(day=1) - timedelta(days=i*30)).replace(day=1)
        month_end = (month_start.replace(month=month_start.month + 1) if month_start.month < 12 
                    else month_start.replace(year=month_start.year + 1, month=1))
        
        month_closed = Ticket.query.filter(
            Ticket.status == 'Cerrado',
            Ticket.closed_at >= month_start,
            Ticket.closed_at < month_end,
            Ticket.clinic_id == clinic_id
        ).all()
        
        month_compliant = sum(1 for t in month_closed if t.compliance_status == 'compliant')
        month_total = len(month_closed)
        compliance_rate = round((month_compliant / month_total * 100) if month_total > 0 else 0, 1)
        
        monthly_compliance.append({
            'month': month_start.strftime('%b %Y'),
            'rate': compliance_rate,
            'total': month_total
        })
    
    monthly_compliance.reverse()
    
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
        'monthly_compliance': monthly_compliance,
        'surgery_distribution': [{'surgery': s.name, 'count': s.ticket_count} for s in surgery_stats]
    }
    
    return render_template('dashboard.html', 
                         kpis=kpis, 
                         recent_tickets=recent_tickets,
                         compliance_stats=compliance_stats,
                         surgery_stats=surgery_stats,
                         modification_stats=modification_stats,
                         chart_data=json.dumps(chart_data))