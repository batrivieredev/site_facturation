import os
from flask import Blueprint, render_template
from app.models import Setting, MailSetting, AppointmentType
from flask import jsonify
from app.models.mail_template import MailTemplate, MailSignature
from app import db

settings_bp = Blueprint('settings', __name__, url_prefix='')

@settings_bp.route('/settings/test_mail', methods=['POST'])
def test_mail():
    from flask import request
    smtp_server = request.form.get('smtp_server')
    smtp_port = request.form.get('smtp_port', type=int)
    smtp_user = request.form.get('smtp_user')
    smtp_password = request.form.get('smtp_password')
    imap_server = request.form.get('imap_server')
    imap_port = request.form.get('imap_port', type=int)
    # Test SMTP
    import smtplib
    try:
        with smtplib.SMTP(smtp_server, smtp_port, timeout=10) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
        smtp_ok = True
    except Exception:
        smtp_ok = False
    # Test IMAP
    import imaplib
    try:
        mail = imaplib.IMAP4_SSL(imap_server, imap_port)
        mail.login(smtp_user, smtp_password)
        mail.logout()
        imap_ok = True
    except Exception:
        imap_ok = False
    return jsonify({'success': smtp_ok and imap_ok})

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
    mail_templates = MailTemplate.query.order_by(MailTemplate.name).all()
    mail_signatures = MailSignature.query.order_by(MailSignature.name).all()
    # Liste des fichiers d'attachement
    upload_dir = os.path.join(os.path.dirname(__file__), '../static/uploads')
    try:
        attachments = [f for f in os.listdir(upload_dir) if not f.startswith('.') and not f.endswith('.md')]
    except Exception:
        attachments = []
    return render_template(
        'settings.html',
        settings=settings,
        mail_settings=mail_settings,
        appointment_types=appointment_types,
        logo_url=logo_url,
        mail_templates=mail_templates,
        mail_signatures=mail_signatures,
        attachments=attachments
    )

# Upload attachment
@settings_bp.route('/settings/upload_attachment', methods=['POST'])
def upload_attachment():
    from flask import request, redirect, url_for, flash
    import os
    file = request.files.get('attachment')
    if not file or not file.filename:
        flash('Aucun fichier sélectionné.', 'danger')
        return redirect(url_for('settings.settings'))
    filename = file.filename.replace(' ', '_')
    upload_dir = os.path.join(os.path.dirname(__file__), '../static/uploads')
    os.makedirs(upload_dir, exist_ok=True)
    file.save(os.path.join(upload_dir, filename))
    flash('Fichier ajouté avec succès.', 'success')
    return redirect(url_for('settings.settings'))

# Delete attachment
@settings_bp.route('/settings/delete_attachment', methods=['POST'])
def delete_attachment():
    from flask import request, redirect, url_for, flash
    import os
    filename = request.form.get('filename')
    if not filename:
        flash('Nom de fichier manquant.', 'danger')
        return redirect(url_for('settings.settings'))

# --- MailTemplate & MailSignature CRUD routes must be top-level, not nested ---

@settings_bp.route('/edit_mail_template/<int:template_id>', methods=['POST'])
def edit_mail_template(template_id):
    print(f"[DEBUG] edit_mail_template called with id={template_id}")
    from flask import request, redirect, url_for, flash
    name = request.form.get('name')
    subject = request.form.get('subject')
    body = request.form.get('body')
    if not name or not body:
        flash('Tous les champs sont obligatoires.', 'danger')
        return redirect(url_for('settings.settings'))
    try:
        template = MailTemplate.query.get(template_id)
        if template:
            template.name = name
            template.subject = subject
            template.body = body
            db.session.commit()
            flash('Mail type modifié avec succès.', 'success')
        else:
            flash('Mail type introuvable.', 'danger')
    except Exception as e:
        db.session.rollback()
        flash(f'Erreur lors de la modification : {str(e)}', 'danger')
    return redirect(url_for('settings.settings'))
@settings_bp.route('/settings/add_mail_template', methods=['POST'])
def add_mail_template():
    from flask import request, redirect, url_for, flash
    name = request.form.get('name')
    subject = request.form.get('subject')
    body = request.form.get('body')
    if not name or not body:
        flash('Tous les champs sont obligatoires.', 'danger')
        return redirect(url_for('settings.settings'))
    try:
        from app.models.mail_template import MailTemplate
        new_template = MailTemplate(name=name, subject=subject, body=body)
        db.session.add(new_template)
        db.session.commit()
        flash('Mail type ajouté avec succès.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erreur lors de l\'ajout : {str(e)}', 'danger')
    return redirect(url_for('settings.settings'))

# CRUD MailSignature
@settings_bp.route('/settings/add_mail_signature', methods=['POST'])
def add_mail_signature():
    from flask import request, redirect, url_for, flash
    name = request.form.get('name')
    signature = request.form.get('signature')
    if not name or not signature:
        flash('Tous les champs sont obligatoires.', 'danger')
        return redirect(url_for('settings.settings'))
    try:
        from app.models.mail_template import MailSignature
        new_signature = MailSignature(name=name, signature=signature)
        db.session.add(new_signature)
        db.session.commit()
        flash('Signature ajoutée avec succès.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erreur lors de l\'ajout : {str(e)}', 'danger')
    return redirect(url_for('settings.settings'))

@settings_bp.route('/settings/add_appointment_type', methods=['POST'])
def add_appointment_type():
    from flask import request, redirect, url_for, flash
    name = request.form.get('name')
    description = request.form.get('description')
    price = request.form.get('price')
    if not name or not price:
        flash('Tous les champs sont obligatoires.', 'danger')
        return redirect(url_for('settings.settings'))
    try:
        price = float(price)
        new_type = AppointmentType(name=name, description=description, price=price)
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
    if not name or not price:
        flash('Tous les champs sont obligatoires.', 'danger')
        return redirect(url_for('settings.settings'))
    try:
        price = float(price)
        appointment_type = AppointmentType.query.get(type_id)
        if appointment_type:
            appointment_type.name = name
            appointment_type.description = description
            appointment_type.price = price
            db.session.commit()
            flash('Type de rendez-vous modifié avec succès.', 'success')
        else:
            flash('Type de rendez-vous introuvable.', 'danger')
    except Exception as e:
        db.session.rollback()
        flash(f'Erreur lors de la modification : {str(e)}', 'danger')
    return redirect(url_for('settings.settings'))
