from flask import Blueprint, render_template
from app.models import Invoice, Appointment, Client, Setting
from app import db

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/api/dashboard_stats')
def dashboard_stats_api():
    from datetime import datetime, timedelta
    now = datetime.now()
    def revenue_sum(start, end):
        return db.session.query(db.func.coalesce(db.func.sum(Invoice.total), 0)).filter(
            Invoice.date >= start,
            Invoice.date < end,
            Invoice.status.in_(['envoyée', 'payée', 'validée'])
        ).scalar()
    today = now.replace(hour=0, minute=0, second=0, microsecond=0)
    week_start = today - timedelta(days=today.weekday())
    month_start = today.replace(day=1)
    year_start = today.replace(month=1, day=1)
    stats = {
        'day': float(revenue_sum(today, today + timedelta(days=1))),
        'week': float(revenue_sum(week_start, week_start + timedelta(days=7))),
        'month': float(revenue_sum(month_start, (month_start + timedelta(days=32)).replace(day=1))),
        'year': float(revenue_sum(year_start, year_start.replace(year=year_start.year + 1))),
        'invoice_count': Invoice.query.count()
    }
    from flask import jsonify
    return jsonify(stats)

@dashboard_bp.route('/')
@dashboard_bp.route('/dashboard')
def dashboard():
    from datetime import datetime, timedelta
    import requests
    from icalendar import Calendar
    from io import BytesIO
    import logging
    from datetime import timezone
    now = datetime.now(timezone.utc)
    # Revenue stats (only issued or paid invoices)
    def revenue_sum(start, end):
        return db.session.query(db.func.coalesce(db.func.sum(Invoice.total), 0)).filter(
            Invoice.date >= start,
            Invoice.date < end,
            Invoice.status.in_(['envoyée', 'payée', 'validée'])
        ).scalar()
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
    # Prepare invoices for display (format date, client, amount)
    invoices_display = []
    for inv in latest_invoices:
        # Get client name if possible
        client_name = f"{inv.client.last_name} {inv.client.first_name}" if getattr(inv, 'client', None) and hasattr(inv.client, 'last_name') and hasattr(inv.client, 'first_name') else ''
        # Format date
        date_str = inv.date.strftime('%d/%m/%Y') if inv.date else ''
        # Format amount
        amount = f"{inv.total:.2f}" if inv.total is not None else "0.00"
        invoices_display.append({
            'number': inv.number,
            'client_name': client_name,
            'date': date_str,
            'amount': amount,
            'status': inv.status
        })
    # Next appointment from Google Calendar (iCal feed)
    settings = Setting.query.first()
    google_agenda_url = settings.google_agenda_url if settings and settings.google_agenda_url else None
    next_appointment_display = None
    error_message = None
    def get_ical_url_from_embed(url):
        import urllib.parse
        if url and "calendar.google.com/calendar/embed" in url:
            parsed = urllib.parse.urlparse(url)
            qs = urllib.parse.parse_qs(parsed.query)
            src = qs.get("src", [None])[0]
            if src:
                return f"https://calendar.google.com/calendar/ical/{src}/public/basic.ics"
        return url
    if google_agenda_url:
        try:
            ical_url = get_ical_url_from_embed(google_agenda_url)
            resp = requests.get(ical_url)
            resp.raise_for_status()
            cal = Calendar.from_ical(resp.content)
            events = []
            for component in cal.walk():
                if component.name == "VEVENT":
                    start = component.get('dtstart').dt
                    end = component.get('dtend').dt
                    summary = str(component.get('summary', ''))
                    description = str(component.get('description', ''))
                    # Handle all-day events (date only)
                    if not isinstance(start, datetime):
                        start = datetime.combine(start, datetime.min.time(), tzinfo=timezone.utc)
                    if start >= now:
                        events.append({
                            'start': start,
                            'end': end,
                            'summary': summary,
                            'description': description
                        })
            events = sorted(events, key=lambda e: e['start'])
            if events:
                event = events[0]
                # Conversion en Europe/Paris
                import pytz
                paris_tz = pytz.timezone('Europe/Paris')
                start_paris = event['start'].astimezone(paris_tz)
                date_str = start_paris.strftime('%d/%m/%Y')
                time_str = start_paris.strftime('%H:%M')
                next_appointment_display = {
                    'client_name': event['summary'],
                    'type': event['description'],
                    'description': '',
                    'date': date_str,
                    'time': time_str
                }
            else:
                error_message = "Aucun événement à venir trouvé dans Google Agenda."
        except Exception as e:
            logging.exception("Erreur lors de la récupération de l'agenda Google")
            error_message = f"Erreur lors de la récupération de l'agenda Google : {str(e)}"
    else:
        # Fallback to local Appointment model if no Google Agenda URL
        next_appointment = Appointment.query.filter(Appointment.date >= now).order_by(Appointment.date.asc()).first()
        if next_appointment:
            client_name = f"{next_appointment.client.last_name} {next_appointment.client.first_name}" if next_appointment.client else ""
            type_name = next_appointment.type.name if next_appointment.type else ""
            description = next_appointment.type.description if next_appointment.type and next_appointment.type.description else ""
            date_str = next_appointment.date.strftime('%d/%m/%Y') if next_appointment.date else ""
            time_str = next_appointment.date.strftime('%H:%M') if next_appointment.date else ""
            next_appointment_display = {
                'client_name': client_name,
                'type': type_name,
                'description': description,
                'date': date_str,
                'time': time_str
            }
    return render_template('dashboard.html', stats=stats, latest_invoices=invoices_display, next_appointment=next_appointment_display, google_agenda_url=google_agenda_url, error_message=error_message)
