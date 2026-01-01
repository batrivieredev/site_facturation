from flask import Blueprint, render_template
from app.models import MailLog, Client
from app import db

mailing_bp = Blueprint('mailing', __name__)

@mailing_bp.route('/mailing')
def mailing():
    from app.models.mail_template import MailTemplate, MailSignature
    from app.models.appointment import AppointmentType
    import os
    mail_logs = MailLog.query.order_by(MailLog.sent_at.desc()).all()
    clients = Client.query.order_by(Client.last_name, Client.first_name).all()
    appointment_types = AppointmentType.query.order_by(AppointmentType.name).all()
    try:
        mail_templates = MailTemplate.query.order_by(MailTemplate.name).all()
        if mail_templates is None:
            mail_templates = []
    except Exception:
        mail_templates = []
    try:
        mail_signatures = MailSignature.query.order_by(MailSignature.name).all() or []
    except Exception:
        mail_signatures = []
    upload_dir = os.path.join('app', 'static', 'uploads')
    try:
        attachments = [f for f in os.listdir(upload_dir) if not f.startswith('.') and not f.endswith('.md')]
    except Exception:
        attachments = []
    return render_template(
        'mailing.html',
        mail_logs=mail_logs,
        clients=clients,
        appointment_types=appointment_types,
        mail_templates=mail_templates,
        mail_signatures=mail_signatures,
        attachments=attachments
    )

# Envoi individuel
@mailing_bp.route('/mailing/send/<int:client_id>', methods=['POST'])
def send_mail_to_client(client_id):
    from flask import request, redirect, url_for, flash
    from app.services.mail_service import send_email
    from app.models.mail_setting import MailSetting
    from app.models.mail_template import MailTemplate, MailSignature
    client = Client.query.get_or_404(client_id)
    mail_settings = MailSetting.query.first()
    subject = request.form['subject']
    body = request.form['body']
    template_id = request.form.get('template')
    signature_id = request.form.get('signature')
    attachment_name = request.form.get('attachment')
    attachment_path = None
    attachment_filename = None
    if attachment_name:
        import os
        upload_dir = os.path.join('app', 'static', 'uploads')
        attachment_path = os.path.join(upload_dir, attachment_name)
        attachment_filename = attachment_name
    if template_id:
        template = MailTemplate.query.get(template_id)
        if template:
            body = template.body + "\n" + body
    if signature_id:
        signature = MailSignature.query.get(signature_id)
        if signature:
            body = body + "\n" + signature.signature
    sender = mail_settings.smtp_user
    recipients = [client.email]
    success = send_email(mail_settings, sender, recipients, subject, body, attachment_path=attachment_path, attachment_filename=attachment_filename)
    if success:
        flash('E-mail envoyé avec succès.', 'success')
    else:
        flash('Erreur lors de l\'envoi de l\'e-mail.', 'danger')
    return redirect(url_for('mailing.mailing'))

# Envoi groupé (CCI)
@mailing_bp.route('/mailing/send_group', methods=['POST'])
def send_mail_group():
    from flask import request, redirect, url_for, flash
    from app.services.mail_service import send_email
    from app.models.mail_setting import MailSetting
    from app.models.mail_template import MailTemplate, MailSignature
    import os
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
    if template_id:
        template = MailTemplate.query.get(template_id)
        if template:
            body = template.body + "\n" + body
    if signature_id:
        signature = MailSignature.query.get(signature_id)
        if signature:
            body = body + "\n" + signature.signature
    sender = mail_settings.smtp_user
    recipients = [c.email for c in clients]
    success = send_email(mail_settings, sender, [], subject, body, bcc=recipients, attachment_path=attachment_path, attachment_filename=attachment_filename)
    if success:
        flash('E-mail groupé envoyé avec succès.', 'success')
    else:
        flash('Erreur lors de l\'envoi du mail groupé.', 'danger')
    return redirect(url_for('mailing.mailing'))
