from flask import Blueprint, render_template
from app.models import Invoice, Appointment, Client
from app import db

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
@dashboard_bp.route('/dashboard')
def dashboard():
    from datetime import datetime, timedelta
    now = datetime.now()
    # Revenue stats
    def revenue_sum(start, end):
        return db.session.query(db.func.coalesce(db.func.sum(Invoice.total), 0)).filter(Invoice.date >= start, Invoice.date < end).scalar()
    today = now.replace(hour=0, minute=0, second=0, microsecond=0)
    week_start = today - timedelta(days=today.weekday())
    month_start = today.replace(day=1)
    year_start = today.replace(month=1, day=1)
    stats = {
        'day': revenue_sum(today, today + timedelta(days=1)),
        'week': revenue_sum(week_start, week_start + timedelta(days=7)),
        'month': revenue_sum(month_start, (month_start + timedelta(days=32)).replace(day=1)),
        'year': revenue_sum(year_start, year_start.replace(year=year_start.year + 1)),
        'invoice_count': Invoice.query.count()
    }
    # Latest invoices
    latest_invoices = Invoice.query.order_by(Invoice.date.desc()).limit(5).all()
    # Next appointment (Google Agenda block)
    next_appointment = Appointment.query.filter(Appointment.date >= now).order_by(Appointment.date.asc()).first()
    return render_template('dashboard.html', stats=stats, latest_invoices=latest_invoices, next_appointment=next_appointment)
