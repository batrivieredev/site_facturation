import smtplib
import imaplib
from app.models.mail_setting import MailSetting
from app.models.mail_log import MailLog
from app import db

def send_email(smtp_settings, sender, recipients, subject, body, bcc=None):
    try:
        with smtplib.SMTP(smtp_settings.smtp_server, smtp_settings.smtp_port) as server:
            server.starttls()
            server.login(smtp_settings.smtp_user, smtp_settings.smtp_password)
            message = f"From: {sender}\nTo: {', '.join(recipients)}\nSubject: {subject}\n\n{body}"
            if bcc:
                recipients += bcc
            server.sendmail(sender, recipients, message)
        log = MailLog(recipient=','.join(recipients), subject=subject, body=body, status='success')
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
