from app import db
from datetime import datetime

class Client(db.Model):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    phone = db.Column(db.String(20))
    address = db.Column(db.String(255))
    status = db.Column(db.String(20))  # honoré, reporté, pas venu
    rdv_type = db.Column(db.String(100))  # type de RDV
    appointments = db.relationship('Appointment', backref='client', lazy=True)
    invoices = db.relationship('Invoice', backref='client', lazy=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
