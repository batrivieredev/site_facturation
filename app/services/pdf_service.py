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
    # Compute logo absolute path if present
    logo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../' + company_settings.logo)) if getattr(company_settings, 'logo', None) else None
    html = render_template('invoices/invoice_pdf.html', invoice=invoice, items=items, client=client, company=company_settings, logo_path=logo_path)
    css_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../static/css/invoice_pdf.css'))
    pdf_buffer = io.BytesIO()
    HTML(string=html, base_url=os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))).write_pdf(pdf_buffer, stylesheets=[CSS(filename=css_path)])
    pdf_buffer.seek(0)
    return pdf_buffer
