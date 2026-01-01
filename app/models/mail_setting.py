from app import db
from datetime import datetime

class MailSetting(db.Model):
    __tablename__ = 'mail_settings'
    id = db.Column(db.Integer, primary_key=True)
    smtp_server = db.Column(db.String(255))
    smtp_port = db.Column(db.Integer)
    smtp_user = db.Column(db.String(120))
    smtp_password = db.Column(db.String(255))
    imap_server = db.Column(db.String(255))
    imap_port = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
