from flask import Blueprint, request, make_response
from flask_login import login_required, current_user
from models import db, Ticket, DischargeTimeSlot
import io
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter
from .utils import _build_tickets_query

exports_bp = Blueprint('exports', __name__)

@exports_bp.route('/ticket/<ticket_id>/pdf')
@login_required
def export_pdf(ticket_id):
    ticket = Ticket.query.filter_by(id=ticket_id, clinic_id=current_user.clinic_id).first_or_404()
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='CustomTitle', parent=styles['Title'], fontSize=20, alignment=TA_CENTER, spaceBottom=20))
    styles.add(ParagraphStyle(name='CustomSubTitle', parent=styles['h2'], fontSize=14, alignment=TA_LEFT, spaceBottom=10, spaceTop=10, textColor=colors.HexColor("#14B8A6")))
    styles.add(ParagraphStyle(name='CustomBodyHead', parent=styles['Normal'], alignment=TA_LEFT, textColor=colors.dimgrey, fontName='Helvetica-Bold'))
    styles.add(ParagraphStyle(name='CustomBodyText', parent=styles['Normal'], alignment=TA_LEFT))

    story = []

    # Helper to handle None values
    def p(text, style='CustomBodyText'):
        return Paragraph(str(text or ''), styles[style])

    def h(text, style='CustomBodyHead'):
        return Paragraph(str(text or ''), styles[style])

    # Title
    story.append(p(f"Detalle de Ticket Home: {ticket.id}", 'CustomTitle'))
    story.append(Spacer(1, 0.2*inch))

    # --- Ticket Information ---
    story.append(p("Información del Ticket", 'CustomSubTitle'))
    ticket_data = [
        [h("Estado"), p(ticket.status)],
        [h("FPA Inicial"), p(ticket.initial_fpa.strftime('%d/%m/%Y %H:%M'))],
        [h("FPA Actual"), p(f"{ticket.current_fpa.strftime('%d/%m/%Y')} {ticket.discharge_time_slot.name if ticket.discharge_time_slot else ''}")],
        [h("Noches de Estancia"), p(ticket.overnight_stays)],
        [h("Creado por"), p(ticket.created_by)],
        [h("Fecha de Creación"), p(ticket.created_at.strftime('%d/%m/%Y %H:%M'))],
        [h("Bloque Horario de Alta"), p(ticket.discharge_time_slot.name if ticket.discharge_time_slot else 'No asignado')],
    ]
    story.append(Table(ticket_data, colWidths=[2*inch, 4*inch], style=TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey), ('VALIGN', (0,0), (-1,-1), 'MIDDLE')
    ])))
    story.append(Spacer(1, 0.2*inch))

    # --- Patient Information ---
    story.append(p("Información del Paciente", 'CustomSubTitle'))
    patient_data = [
        [h("Nombre Completo"), p(ticket.patient.full_name)],
        [h("RUT"), p(ticket.patient.rut)],
        [h("Edad"), p(f"{ticket.patient.age} años")],
        [h("Sexo"), p(ticket.patient.sex)],
    ]
    story.append(Table(patient_data, colWidths=[2*inch, 4*inch], style=TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey), ('VALIGN', (0,0), (-1,-1), 'MIDDLE')
    ])))
    story.append(Spacer(1, 0.2*inch))

    # --- Surgery Information ---
    story.append(p("Información Quirúrgica", 'CustomSubTitle'))
    surgery_data = [
        [h("Cirugía"), p(ticket.surgery.name)],
        [h("Técnica"), p(ticket.technique.name)],
        [h("Médico Tratante"), p(ticket.attending_doctor.name if ticket.attending_doctor else 'N/A')],
        [h("Fin de Pabellón"), p(ticket.pavilion_end_time.strftime('%d/%m/%Y %H:%M'))],
    ]
    story.append(Table(surgery_data, colWidths=[2*inch, 4*inch], style=TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey), ('VALIGN', (0,0), (-1,-1), 'MIDDLE')
    ])))
    story.append(Spacer(1, 0.2*inch))

    # --- Modification History ---
    if ticket.modifications:
        story.append(p("Historial de Modificaciones", 'CustomSubTitle'))
        
        mod_data = [[
            h('Fecha'), h('FPA Anterior'), h('FPA Nueva'), h('Bloque'), 
            h('Usuario'), h('Motivo'), h('Justificación')
        ]]
        
        modifications = sorted(ticket.modifications, key=lambda m: m.modified_at)

        for mod in modifications:
            slot = DischargeTimeSlot.query.filter_by(id=mod.ticket.discharge_slot_id).first()
            slot_name = slot.name if slot else "N/A"

            mod_data.append([
                p(mod.modified_at.strftime('%d/%m/%Y %H:%M')),
                p(mod.previous_fpa.strftime('%d/%m/%Y %H:%M')),
                p(f"{mod.new_fpa.strftime('%d/%m/%Y')} {slot_name}"),
                p(slot_name),
                p(mod.modified_by),
                p(mod.reason),
                p(mod.justification)
            ])

        story.append(Table(mod_data, colWidths=[0.8*inch, 0.8*inch, 0.8*inch, 1*inch, 0.8*inch, 1*inch, 1.2*inch], style=TableStyle([
            ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('BACKGROUND', (0,0), (-1,0), colors.lightgrey)
        ])))
        story.append(Spacer(1, 0.2*inch))
    
    # --- Closure/Annulment Info ---
    if ticket.status in ['Anulado']:
        story.append(p(f"Información de {ticket.status}", 'CustomSubTitle'))
        info_data = []
        if ticket.status == TICKET_STATUS_ANULADO: # Anulado
            info_data.extend([
                [h("Fecha de Anulación"), p(ticket.annulled_at.strftime('%d/%m/%Y %H:%M') if ticket.annulled_at else 'N/A')],
                [h("Anulado por"), p(ticket.annulled_by)],
                [h("Razón de Anulación"), p(ticket.annulled_reason)],
            ])
        
        story.append(Table(info_data, colWidths=[2*inch, 4*inch], style=TableStyle([
            ('GRID', (0,0), (-1,-1), 0.5, colors.grey), ('VALIGN', (0,0), (-1,-1), 'MIDDLE')
        ])))

    doc.build(story)
    buffer.seek(0)
    response = make_response(buffer.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename="ticket_{ticket.id}.pdf"'
    return response

@exports_bp.route('/tickets/reports/excel')
@login_required
def export_excel():
    filters = {
        'status': request.args.get('status', ''),
        'surgery': request.args.get('surgery', ''),
        'date_from': request.args.get('date_from', ''),
        'date_to': request.args.get('date_to', ''),
    }
    query = _build_tickets_query(filters)
    tickets = query.order_by(Ticket.created_at.desc()).all()
    
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Reporte Tickets"
    
    headers = [
        'N° Ticket', 'Estado', 'RUT Paciente', 'Nombre Completo', 'Cirugía', 
        'Técnica', 'Médico', 'FPA Inicial', 'FPA Actual', 'Noches de Estancia',
        'Creado Por', 'Fecha Creación'
    ]
    
    for i in range(1, 6):
        headers.extend([
            f'Fecha Modificación {i}',
            f'Bloque Modificación {i}',
            f'Usuario Modificación {i}',
            f'Motivo Modificación {i}',
            f'Justificación Modificación {i}'
        ])
        
    ws.append(headers)
    
    for ticket in tickets:
        row = [
            ticket.id,
            ticket.status,
            ticket.patient.rut,
            ticket.patient.full_name,
            ticket.surgery.name,
            ticket.technique.name,
            ticket.attending_doctor.name if ticket.attending_doctor else 'N/A',
            ticket.initial_fpa.strftime('%Y-%m-%d %H:%M'),
            f"{ticket.current_fpa.strftime('%Y-%m-%d')} {ticket.discharge_time_slot.name if ticket.discharge_time_slot else ''}",
            ticket.overnight_stays,
            ticket.created_by,
            ticket.created_at.strftime('%Y-%m-%d %H:%M')
        ]
        
        modifications = sorted(ticket.modifications, key=lambda m: m.modified_at)
        
        for i in range(5):
            if i < len(modifications):
                mod = modifications[i]
                # Find the discharge slot for the modification
                slot = DischargeTimeSlot.query.filter_by(id=mod.ticket.discharge_slot_id).first()
                slot_name = slot.name if slot else "N/A"
                
                row.extend([
                    f"{mod.new_fpa.strftime('%Y-%m-%d')} {slot_name}",
                    slot_name,
                    mod.modified_by,
                    mod.reason,
                    mod.justification
                ])
            else:
                row.extend(['', '', '', '', ''])
                
        ws.append(row)
        
    buffer = io.BytesIO()
    wb.save(buffer)
    buffer.seek(0)
    
    response = make_response(buffer.getvalue())
    response.headers['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    response.headers['Content-Disposition'] = f'attachment; filename="reporte_tickets.xlsx"'
    return response
