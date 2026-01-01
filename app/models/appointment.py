from app import db
from datetime import datetime

class AppointmentType(db.Model):
    __tablename__ = 'appointment_types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))  # description for invoices
    price = db.Column(db.Numeric(10, 2), nullable=False)
    duration = db.Column(db.Integer)  # duration in minutes
    agenda_link_id = db.Column(db.Integer, db.ForeignKey('agenda_links.id'))
    appointments = db.relationship('Appointment', backref='type', lazy=True)

class Appointment(db.Model):
    __tablename__ = 'appointments'
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey('appointment_types.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20))  # honoré, reporté, pas venu
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
