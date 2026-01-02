from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import MailLog, Client
from app.models.mail_setting import MailSetting
from app.models.mail_template import MailTemplate, MailSignature
from app.models.appointment import AppointmentType
from app import db
from app.services.mail_service import send_email
import os

mailing_bp = Blueprint('mailing', __name__)

@mailing_bp.route('/mailing')
def mailing():
    mail_logs = MailLog.query.order_by(MailLog.sent_at.desc()).all()
    clients = Client.query.order_by(Client.last_name, Client.first_name).all()
    appointment_types = AppointmentType.query.order_by(AppointmentType.name).all()

    mail_templates = MailTemplate.query.order_by(MailTemplate.name).all()
    mail_signatures = MailSignature.query.order_by(MailSignature.name).all()

    subject = ""
    body = ""
    selected_template_id = None
    selected_signature_id = None

    # Mail type par défaut
    if mail_templates:
        default_template = mail_templates[0]
        subject = default_template.subject or ""
        body = default_template.body or ""
        selected_template_id = default_template.id

    # Signature par défaut
    if mail_signatures:
        default_signature = mail_signatures[0]
        body = body.rstrip() + "\n\n" + default_signature.signature
        selected_signature_id = default_signature.id

    upload_dir = os.path.join('app', 'static', 'uploads')
    try:
        attachments = [
            f for f in os.listdir(upload_dir)
            if not f.startswith('.') and not f.endswith('.md')
        ]
    except Exception:
        attachments = []

    return render_template(
        'mailing.html',
        mail_logs=mail_logs,
        clients=clients,
        appointment_types=appointment_types,
        mail_templates=mail_templates,
        mail_signatures=mail_signatures,
        attachments=attachments,
        subject=subject,
        body=body,
        selected_template_id=selected_template_id,
        selected_signature_id=selected_signature_id
    )

@mailing_bp.route('/mailing/send/<int:client_id>', methods=['POST'])
def send_mail_to_client(client_id):
    client = Client.query.get_or_404(client_id)
    mail_settings = MailSetting.query.first()
    subject = request.form['subject']
    body = request.form['body']
    attachment_name = request.form.get('attachment')
    attachment_path = None
    attachment_filename = None
    if attachment_name:
        upload_dir = os.path.join('app', 'static', 'uploads')
        attachment_path = os.path.join(upload_dir, attachment_name)
        attachment_filename = attachment_name
    sender = mail_settings.smtp_user
    recipients = [client.email]
    success = send_email(
        mail_settings, sender, recipients, subject, body,
        attachment_path=attachment_path, attachment_filename=attachment_filename
    )
    if success:
        flash('E-mail envoyé avec succès.', 'success')
    else:
        flash('Erreur lors de l\'envoi de l\'e-mail.', 'danger')
    return redirect(url_for('mailing.mailing'))

@mailing_bp.route('/mailing/send_group', methods=['POST'])
def send_mail_group():
    filter_status = request.form.get('status')
    filter_type = request.form.get('type')
    template_id = request.form.get('template')
    signature_id = request.form.get('signature')
    attachment_name = request.form.get('attachment')
    attachment_path = None
    attachment_filename = None
    if attachment_name:
        upload_dir = os.path.join('app', 'static', 'uploads')
        attachment_path = os.path.join(upload_dir, attachment_name)
        attachment_filename = attachment_name

    clients_query = Client.query
    if filter_status:
        clients_query = clients_query.filter_by(status=filter_status)
    if filter_type:
        clients_query = clients_query.join(Client.appointments).filter_by(type_id=filter_type)
    clients = clients_query.all()

    mail_settings = MailSetting.query.first()
    subject = request.form['subject']
    body = request.form['body']
    sender = mail_settings.smtp_user
    recipients = [c.email for c in clients]

    success = send_email(
        mail_settings, sender, [], subject, body,
        bcc=recipients, attachment_path=attachment_path, attachment_filename=attachment_filename
    )
    if success:
        flash('E-mail groupé envoyé avec succès.', 'success')
    else:
        flash('Erreur lors de l\'envoi du mail groupé.', 'danger')
    return redirect(url_for('mailing.mailing'))
