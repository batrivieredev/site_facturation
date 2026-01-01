import io
from flask import render_template
import os
from weasyprint import HTML, CSS

def generate_invoice_pdf(invoice, items, client, company_settings):
    # Add rdv_type_description for client if possible
    if hasattr(client, 'rdv_type') and client.rdv_type:
        from app.models import AppointmentType
        appt_type = AppointmentType.query.filter_by(name=client.rdv_type).first()
        client.rdv_type_description = appt_type.description if appt_type and appt_type.description else ''
    else:
        client.rdv_type_description = ''
    html = render_template('invoices/invoice_pdf.html', invoice=invoice, items=items, client=client, company=company_settings)
    css_path = os.path.join(os.path.dirname(__file__), '../static/css/invoice.css')
    pdf_buffer = io.BytesIO()
    HTML(string=html).write_pdf(pdf_buffer, stylesheets=[CSS(filename=css_path)])
    pdf_buffer.seek(0)
    return pdf_buffer
