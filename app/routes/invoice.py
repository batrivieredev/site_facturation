from flask import Blueprint, render_template
from app.models import Invoice, Client, InvoiceItem, AppointmentType
from app import db

invoice_bp = Blueprint('invoice', __name__)

@invoice_bp.route('/invoices')
def invoices():
    from flask import request
    query = Invoice.query
    client_id = request.args.get('client_id')
    status = request.args.get('status')
    search = request.args.get('search')
    if client_id:
        query = query.filter_by(client_id=client_id)
    if status:
        query = query.filter_by(status=status)
    if search:
        query = query.filter(Invoice.number.ilike(f"%{search}%"))
    invoices = query.order_by(Invoice.date.desc()).all()
    appointment_types = AppointmentType.query.order_by(AppointmentType.name).all()
    clients = Client.query.order_by(Client.last_name, Client.first_name).all()
    return render_template('invoices.html', invoices=invoices, appointment_types=appointment_types, clients=clients)

# PDF generation route
@invoice_bp.route('/invoices/<int:invoice_id>/pdf')
def invoice_pdf(invoice_id):
    from flask import send_file, abort
    from app.services.pdf_service import generate_invoice_pdf
    invoice = Invoice.query.get_or_404(invoice_id)
    client = invoice.client
    items = invoice.items
    from app.models.setting import Setting
    company_settings = Setting.query.first()
    pdf_buffer = generate_invoice_pdf(invoice, items, client, company_settings)
    return send_file(pdf_buffer, as_attachment=True, download_name=f"facture_{invoice.number}.pdf", mimetype='application/pdf')

# Email sending route
@invoice_bp.route('/invoices/<int:invoice_id>/send', methods=['POST'])
def send_invoice(invoice_id):
    from flask import redirect, url_for, flash
    from app.services.mail_service import send_email
    invoice = Invoice.query.get_or_404(invoice_id)
    client = invoice.client
    from app.models.mail_setting import MailSetting
    mail_settings = MailSetting.query.first()
    subject = f"Votre facture {invoice.number}"
    body = f"Bonjour {client.first_name},\n\nVeuillez trouver votre facture en pièce jointe."
    sender = mail_settings.smtp_user
    recipients = [client.email]
    success = send_email(mail_settings, sender, recipients, subject, body)
    if success:
        flash('Facture envoyée avec succès.', 'success')
        invoice.status = 'envoyée'
        from app import db
        db.session.commit()
    else:
        flash('Erreur lors de l\'envoi de la facture.', 'danger')
    return redirect(url_for('invoice.invoices'))
