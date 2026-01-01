from flask import Blueprint, render_template
from app.models import Setting, MailSetting, AppointmentType
from app import db

settings_bp = Blueprint('settings', __name__)

@settings_bp.route('/settings', methods=['GET'])
def settings():
    settings = Setting.query.first()
    mail_settings = MailSetting.query.first()
    appointment_types = AppointmentType.query.order_by(AppointmentType.name).all()
    return render_template('settings.html', settings=settings, mail_settings=mail_settings, appointment_types=appointment_types)

@settings_bp.route('/settings/add_appointment_type', methods=['POST'])
def add_appointment_type():
    from flask import request, redirect, url_for, flash
    name = request.form.get('name')
    price = request.form.get('price')
    duration = request.form.get('duration')
    if not name or not price or not duration:
        flash('Tous les champs sont obligatoires.', 'danger')
        return redirect(url_for('settings.settings'))
    try:
        price = float(price)
        duration = int(duration)
        new_type = AppointmentType(name=name, price=price, duration=duration)
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
