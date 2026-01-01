from flask import Blueprint, render_template
from app.models import MailLog, Client
from app import db

mailing_bp = Blueprint('mailing', __name__)

@mailing_bp.route('/mailing')
def mailing():
    mail_logs = MailLog.query.order_by(MailLog.sent_at.desc()).all()
    return render_template('mailing.html', mail_logs=mail_logs)

# Envoi individuel
@mailing_bp.route('/mailing/send/<int:client_id>', methods=['POST'])
def send_mail_to_client(client_id):
    from flask import request, redirect, url_for, flash
    from app.services.mail_service import send_email
    from app.models.mail_setting import MailSetting
    client = Client.query.get_or_404(client_id)
    mail_settings = MailSetting.query.first()
    subject = request.form['subject']
    body = request.form['body']
    sender = mail_settings.smtp_user
    recipients = [client.email]
    success = send_email(mail_settings, sender, recipients, subject, body)
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
    filter_status = request.form.get('status')
    filter_type = request.form.get('type')
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
    success = send_email(mail_settings, sender, [], subject, body, bcc=recipients)
    if success:
        flash('E-mail groupé envoyé avec succès.', 'success')
    else:
        flash('Erreur lors de l\'envoi du mail groupé.', 'danger')
    return redirect(url_for('mailing.mailing'))
