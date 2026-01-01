from flask import Blueprint, render_template
from app.models import Invoice, Client, InvoiceItem, AppointmentType
from app import db

from flask import send_file, abort, url_for
invoice_bp = Blueprint('invoice', __name__)

@invoice_bp.route('/invoices/<int:invoice_id>', methods=['GET', 'POST'])
def view_invoice(invoice_id):
    from flask import render_template, abort, request, redirect, url_for, flash
    from app.models.setting import Setting
    invoice = Invoice.query.get_or_404(invoice_id)
    client = invoice.client
    items = invoice.items if hasattr(invoice, 'items') else []
    company = Setting.query.first()
    if request.args.get('modal') == '1':
        return render_template('invoice_view.html', invoice=invoice, client=client, items=items, company=company)
    if request.method == 'POST':
        new_status = request.form.get('status')
        # No required fields check, just update status if valid
        if new_status in ['brouillon', 'validée', 'envoyée', 'payée']:
            invoice.status = new_status
            db.session.commit()
            flash('Statut de la facture mis à jour.', 'success')
            return redirect(url_for('invoice.invoices'))
        else:
            flash('Statut invalide.', 'danger')
            return redirect(url_for('invoice.view_invoice', invoice_id=invoice_id))
    # Add rdv_type_description for client if possible
    if hasattr(client, 'rdv_type') and client.rdv_type:
        # Try to get description from AppointmentType
        from app.models import AppointmentType
        appt_type = AppointmentType.query.filter_by(name=client.rdv_type).first()
        client.rdv_type_description = appt_type.description if appt_type and appt_type.description else ''
    else:
        client.rdv_type_description = ''
    return render_template('invoice_view.html', invoice=invoice, client=client, items=items, company=company)

@invoice_bp.route('/invoices')
def invoices():
    from flask import request
    query = Invoice.query
    client_id = request.args.get('client_id')
    status = request.args.get('status')
    search_name = request.args.get('search_name')
    search_date = request.args.get('search_date')
    if client_id:
        query = query.filter_by(client_id=client_id)
    if status:
        query = query.filter_by(status=status)
    if search_name:
        query = query.join(Client).filter(
            (Invoice.number.ilike(f"%{search_name}%")) |
            (Client.last_name.ilike(f"%{search_name}%")) |
            (Client.first_name.ilike(f"%{search_name}%"))
        )
    if search_date:
        query = query.filter(db.cast(Invoice.date, db.String).like(f"{search_date}%"))
    invoices = query.order_by(Invoice.date.desc()).all()
    appointment_types = AppointmentType.query.order_by(AppointmentType.name).all()
    clients = Client.query.order_by(Client.last_name, Client.first_name).all()
    # Add client_name and amount for template compatibility
    for invoice in invoices:
        invoice.client_name = invoice.client.last_name + ' ' + invoice.client.first_name if invoice.client else ''
        invoice.amount = invoice.total if hasattr(invoice, 'total') else 0
        invoice.status_display = invoice.status if hasattr(invoice, 'status') else ''
    return render_template('invoices.html', invoices=invoices, appointment_types=appointment_types, clients=clients)

@invoice_bp.route('/invoices', methods=['POST'])
def create_invoice():
    from flask import request, redirect, url_for, flash
    # Si la requête contient uniquement 'status', c'est une modification de statut, on redirige vers la vue facture
    if set(request.form.keys()) == {'status'}:
        invoice_id = request.args.get('invoice_id') or request.form.get('invoice_id')
        if invoice_id:
            return redirect(url_for('invoice.invoices'))
        return redirect(url_for('invoice.invoices'))
    # Sinon, c'est une création de facture
    if 'client' not in request.form:
        return redirect(url_for('invoice.invoices'))
    client_id = request.form.get('client')
    appointment_type_id = request.form.get('appointment_type')
    price = request.form.get('price')
    date = request.form.get('date')
    payment_method = request.form.get('payment_method')
    from app.models import AppointmentType, InvoiceItem
    appointment_type = AppointmentType.query.get(appointment_type_id)
    from app.models.invoice import Invoice
    import datetime
    now = datetime.datetime.now()
    year = now.year
    month = f"{now.month:02d}"
    chrono = Invoice.query.filter(db.extract('year', Invoice.date) == year, db.extract('month', Invoice.date) == now.month).count() + 1
    number = f"F{year}{month}-{chrono}"
    if not client_id or not price or not payment_method:
        flash("Tous les champs obligatoires doivent être remplis pour créer une facture.", "danger")
        return redirect(url_for('invoice.invoices'))
    invoice = Invoice(
        client_id=client_id,
        number=number,
        date=datetime.datetime.strptime(date, "%Y-%m-%d") if date else datetime.datetime.now(),
        status='brouillon',
        total=0,
        payment_method=payment_method
    )
    db.session.add(invoice)
    db.session.flush()  # Get invoice.id before commit
    item = InvoiceItem(
        invoice_id=invoice.id,
        description=appointment_type.description or appointment_type.name,
        quantity=1,
        unit_price=appointment_type.price,
        total=appointment_type.price,
    )
    db.session.add(item)
    db.session.flush()
    # Met à jour le total de la facture avec la somme des items
    invoice.total = sum(i.total for i in invoice.items)
    db.session.commit()
    flash('Facture créée avec succès.', 'success')
    return redirect(url_for('invoice.invoices'))

# PDF generation route
@invoice_bp.route('/invoices/<int:invoice_id>/pdf')
def invoice_pdf(invoice_id):
    from flask import send_file, abort
    from app.services.pdf_service import generate_invoice_pdf
    invoice = Invoice.query.get_or_404(invoice_id)
    client = invoice.client
    items = invoice.items
    # Add rdv_type_description for client if possible
    if hasattr(client, 'rdv_type') and client.rdv_type:
        from app.models import AppointmentType
        appt_type = AppointmentType.query.filter_by(name=client.rdv_type).first()
        client.rdv_type_description = appt_type.description if appt_type and appt_type.description else ''
    else:
        client.rdv_type_description = ''
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

@invoice_bp.route('/invoices/<int:invoice_id>/delete', methods=['POST'])
def delete_invoice(invoice_id):
    from flask import redirect, url_for, flash
    invoice = Invoice.query.get_or_404(invoice_id)
    # Supprimer d'abord tous les items liés à la facture
    for item in invoice.items:
        db.session.delete(item)
    db.session.delete(invoice)
    db.session.commit()
    flash('Facture supprimée avec succès.', 'success')
    return redirect(url_for('invoice.invoices'))
