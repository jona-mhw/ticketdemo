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

    # Colors
    teal_color = colors.HexColor("#008080")
    light_teal_color = colors.HexColor("#E0F2F1")
    white_color = colors.white
    black_color = colors.black

    # Styles
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='MainTitle', fontSize=22, textColor=white_color, fontName='Helvetica-Bold', alignment=TA_LEFT))
    styles.add(ParagraphStyle(name='TicketNumber', fontSize=14, textColor=black_color, fontName='Helvetica', alignment=TA_CENTER))
    styles.add(ParagraphStyle(name='PatientName', fontSize=16, textColor=black_color, fontName='Helvetica-Bold', alignment=TA_CENTER))
    styles.add(ParagraphStyle(name='SectionTitle', fontSize=12, textColor=white_color, fontName='Helvetica', alignment=TA_LEFT))
    styles.add(ParagraphStyle(name='FieldLabel', fontSize=14, textColor=black_color, fontName='Helvetica', alignment=TA_LEFT))
    styles.add(ParagraphStyle(name='FieldValue', fontSize=14, textColor=black_color, fontName='Helvetica-Bold', alignment=TA_CENTER))
    styles.add(ParagraphStyle(name='DoctorName', fontSize=14, textColor=white_color, fontName='Helvetica-Bold', alignment=TA_LEFT))
    styles.add(ParagraphStyle(name='ModificationLabel', fontSize=12, textColor=black_color, fontName='Helvetica', alignment=TA_LEFT))
    styles.add(ParagraphStyle(name='ModificationValue', fontSize=12, textColor=black_color, fontName='Helvetica', alignment=TA_CENTER))
    styles.add(ParagraphStyle(name='ModificationReason', fontSize=12, textColor=black_color, fontName='Helvetica', alignment=TA_LEFT))
    styles.add(ParagraphStyle(name='LogoPlaceholder', fontSize=12, textColor=colors.grey, fontName='Helvetica', alignment=TA_RIGHT))

    # Document
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)

    # Story
    story = []

    # Background
    def background(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(teal_color)
        canvas.rect(0, 0, doc.width + doc.leftMargin * 2, doc.height + doc.topMargin * 2, fill=1, stroke=0)
        canvas.restoreState()

    # Header
    header_data = [
        [Paragraph("Programación del Alta", styles['MainTitle']), Paragraph(f"Ticket N°<br/>{ticket.id}", styles['TicketNumber'])]
    ]
    header_table = Table(header_data, colWidths=[5*inch, 1.5*inch])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BACKGROUND', (1, 0), (1, 0), light_teal_color),
        ('BOX', (1, 0), (1, 0), 1, black_color),
        ('LEFTPADDING', (0, 0), (0, 0), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 0.2*inch))

    # Patient
    patient_data = [
        [Paragraph("Paciente:", styles['FieldLabel']), Paragraph(ticket.patient.full_name, styles['PatientName'])]
    ]
    patient_table = Table(patient_data, colWidths=[1.5*inch, 4*inch])
    patient_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), light_teal_color),
        ('BOX', (0, 0), (-1, -1), 2, white_color),
        ('ROUNDEDCORNERS', [10, 10, 10, 10]),
        ('LEFTPADDING', (0, 0), (0, 0), 10),
        ('RIGHTPADDING', (1, 0), (1, 0), 10),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(patient_table)
    story.append(Spacer(1, 0.2*inch))

    # Discharge Date
    discharge_title = Paragraph(f"Fecha probable de alta ({ticket.overnight_stays} días de pernocte)", styles['SectionTitle'])
    story.append(discharge_title)
    story.append(Spacer(1, 0.1*inch))

    discharge_data = [
        [Paragraph("Fecha:", styles['FieldLabel']), Paragraph(ticket.current_fpa.strftime('%d/%m/%Y'), styles['FieldValue'])],
        [Paragraph("Hora (entre):", styles['FieldLabel']), Paragraph(ticket.discharge_time_slot.name if ticket.discharge_time_slot else '', styles['FieldValue'])]
    ]
    discharge_table = Table(discharge_data, colWidths=[1.5*inch, 4*inch])
    discharge_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), white_color),
        ('BOX', (0, 0), (-1, -1), 2, white_color),
        ('ROUNDEDCORNERS', [10, 10, 10, 10]),
        ('LEFTPADDING', (0, 0), (0, 0), 10),
        ('RIGHTPADDING', (1, 0), (1, 0), 10),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(discharge_table)
    story.append(Spacer(1, 0.2*inch))

    # Doctor
    doctor_name = Paragraph(f"Médico tratante: {ticket.attending_doctor.name if ticket.attending_doctor else 'N/A'}", styles['DoctorName'])
    story.append(doctor_name)
    story.append(Spacer(1, 0.4*inch))

    # Validation & Modification
    validation_data = [
        [Paragraph("Validación", styles['ModificationLabel']), Paragraph("Firma cirujano", styles['ModificationLabel']), None],
        [Paragraph("Modificación", styles['ModificationLabel']), Paragraph("Firma cirujano", styles['ModificationLabel']), None],
        [None, Paragraph("Nueva hora y fecha de alta", styles['ModificationLabel']), None]
    ]
    validation_table = Table(validation_data, colWidths=[1.5*inch, 2*inch, 2.5*inch])
    validation_table.setStyle(TableStyle([
        ('BOX', (2, 0), (2, 0), 1, black_color),
        ('BOX', (2, 1), (2, 1), 1, black_color),
        ('BOX', (2, 2), (2, 2), 1, black_color),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(validation_table)
    story.append(Spacer(1, 0.2*inch))

    # Modification Reason
    if ticket.modifications:
        last_mod = sorted(ticket.modifications, key=lambda m: m.modified_at)[-1]
        reason = last_mod.reason or ""
    else:
        reason = ""
    
    modification_reason_data = [
        [Paragraph("Motivo modificación:", styles['ModificationReason'])],
        [Paragraph(reason, styles['ModificationReason'])]
    ]
    modification_reason_table = Table(modification_reason_data, colWidths=[6.5*inch])
    modification_reason_table.setStyle(TableStyle([
        ('BOX', (0, 1), (0, 1), 1, black_color),
        ('TOPPADDING', (0, 1), (0, 1), 20),
    ]))
    story.append(modification_reason_table)
    story.append(Spacer(1, 0.5*inch))

    # Footer
    footer_data = [
        [Paragraph("[logo]", styles['LogoPlaceholder'])]
    ]
    footer_table = Table(footer_data, colWidths=[6.5*inch])
    story.append(footer_table)

    # Build
    doc.build(story, onFirstPage=background, onLaterPages=background)
    
    buffer.seek(0)
    response = make_response(buffer.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'inline; filename="ticket_{ticket.id}.pdf"'
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
