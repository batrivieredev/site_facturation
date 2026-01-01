from app import db
from datetime import datetime

class MailLog(db.Model):
    __tablename__ = 'mail_logs'
    id = db.Column(db.Integer, primary_key=True)
    recipient = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(255))
    body = db.Column(db.Text)
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20))  # success, failed
