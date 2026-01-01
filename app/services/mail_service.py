import smtplib
import imaplib
from app.models.mail_setting import MailSetting
from app.models.mail_log import MailLog
from app import db
import os
from flask import current_app

def send_email(smtp_settings, sender, recipients, subject, body, bcc=None, attachment_path=None, attachment_filename=None):
    try:
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        from email.mime.base import MIMEBase
        from email import encoders

        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = ', '.join(recipients)
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        if attachment_path and attachment_filename:
            with open(attachment_path, 'rb') as f:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename="{attachment_filename}"')
                msg.attach(part)

        all_recipients = recipients.copy()
        if bcc:
            all_recipients += bcc

        with smtplib.SMTP(smtp_settings.smtp_server, smtp_settings.smtp_port) as server:
            server.starttls()
            server.login(smtp_settings.smtp_user, smtp_settings.smtp_password)
            server.sendmail(sender, all_recipients, msg.as_string())
        log = MailLog(recipient=','.join(all_recipients), subject=subject, body=body, status='success')
        db.session.add(log)
        db.session.commit()
        return True
    except Exception as e:
        log = MailLog(recipient=','.join(recipients), subject=subject, body=body, status='failed')
        db.session.add(log)
        db.session.commit()
        return False

def test_imap_connection(imap_settings):
    try:
        mail = imaplib.IMAP4_SSL(imap_settings.imap_server, imap_settings.imap_port)
        mail.login(imap_settings.smtp_user, imap_settings.smtp_password)
        mail.logout()
        return True
    except Exception:
        return False
