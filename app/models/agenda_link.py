from app import db
from datetime import datetime

class AgendaLink(db.Model):
    __tablename__ = 'agenda_links'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False)
    appointment_types = db.relationship('AppointmentType', backref='agenda_link', lazy=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
