from flask import Blueprint, render_template
from app.models import Setting, MailSetting, AppointmentType
from app import db

settings_bp = Blueprint('settings', __name__)

@settings_bp.route('/settings', methods=['GET', 'POST'])
def settings():
    from flask import request, redirect, url_for, flash
    settings = Setting.query.first()
    mail_settings = MailSetting.query.first()
    appointment_types = AppointmentType.query.order_by(AppointmentType.name).all()
    if request.method == 'POST':
        company_name = request.form.get('company_name')
        siret = request.form.get('siret')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        address = request.form.get('address')
        phone = request.form.get('phone')
        email = request.form.get('email')
        logo_file = request.files.get('logo')
        google_agenda_url = request.form.get('google_agenda_url')
        if not settings:
            settings = Setting()
            db.session.add(settings)
        settings.company_name = company_name
        settings.siret = siret
        settings.first_name = first_name
        settings.last_name = last_name
        settings.address = address
        settings.phone = phone
        settings.email = email
        settings.google_agenda_url = google_agenda_url
        import os
        if logo_file and logo_file.filename:
            filename = logo_file.filename.replace(' ', '_')
            upload_dir = os.path.join(os.path.dirname(__file__), '../static/uploads')
            os.makedirs(upload_dir, exist_ok=True)
            logo_path = os.path.join(upload_dir, filename)
            logo_file.save(logo_path)
            # Store relative path for use in templates
            settings.logo = f'static/uploads/{filename}'
        db.session.commit()
        flash('Informations entreprise enregistrées.', 'success')
        return redirect(url_for('settings.settings'))
    import os
    logo_url = None
    if settings and settings.logo:
        logo_url = url_for('static', filename=f'uploads/{os.path.basename(settings.logo)}')
    return render_template('settings.html', settings=settings, mail_settings=mail_settings, appointment_types=appointment_types, logo_url=logo_url)

@settings_bp.route('/settings/add_appointment_type', methods=['POST'])
def add_appointment_type():
    from flask import request, redirect, url_for, flash
    name = request.form.get('name')
    description = request.form.get('description')
    price = request.form.get('price')
    duration = request.form.get('duration')
    if not name or not price or not duration:
        flash('Tous les champs sont obligatoires.', 'danger')
        return redirect(url_for('settings.settings'))
    try:
        price = float(price)
        duration = int(duration)
        new_type = AppointmentType(name=name, description=description, price=price, duration=duration)
        db.session.add(new_type)
        db.session.commit()
        flash('Type de rendez-vous ajouté avec succès.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erreur lors de l\'ajout : {str(e)}', 'danger')
    return redirect(url_for('settings.settings'))

@settings_bp.route('/settings/edit_appointment_type/<int:type_id>', methods=['POST'])
def edit_appointment_type(type_id):
    from flask import request, redirect, url_for, flash
    name = request.form.get('name')
    description = request.form.get('description')
    price = request.form.get('price')
    duration = request.form.get('duration')
    if not name or not price or not duration:
        flash('Tous les champs sont obligatoires.', 'danger')
        return redirect(url_for('settings.settings'))
    try:
        price = float(price)
        duration = int(duration)
        appointment_type = AppointmentType.query.get(type_id)
        if appointment_type:
            appointment_type.name = name
            appointment_type.description = description
            appointment_type.price = price
            appointment_type.duration = duration
            db.session.commit()
            flash('Type de rendez-vous modifié avec succès.', 'success')
        else:
            flash('Type de rendez-vous introuvable.', 'danger')
    except Exception as e:
        db.session.rollback()
        flash(f'Erreur lors de la modification : {str(e)}', 'danger')
    return redirect(url_for('settings.settings'))
