from flask import Blueprint, render_template
from app.models import Client, Appointment, AppointmentType
from app import db

client_bp = Blueprint('client', __name__)

@client_bp.route('/clients')
def clients():
    clients = Client.query.order_by(Client.last_name, Client.first_name).all()
    appointment_types = AppointmentType.query.order_by(AppointmentType.name).all()
    return render_template('clients.html', clients=clients, appointment_types=appointment_types)

# CRUD, historique RDV, accès factures, statut RDV
@client_bp.route('/clients/<int:client_id>')
def client_detail(client_id):
    client = Client.query.get_or_404(client_id)
    appointments = client.appointments
    invoices = client.invoices
    return render_template('client_detail.html', client=client, appointments=appointments, invoices=invoices)

@client_bp.route('/clients/edit/<int:client_id>', methods=['POST'])
def edit_client(client_id):
    from flask import request, redirect, url_for, flash
    client = Client.query.get_or_404(client_id)
    client.last_name = request.form.get('last_name')
    client.first_name = request.form.get('first_name')
    client.email = request.form.get('email')
    client.phone = request.form.get('phone')
    client.address = request.form.get('address')
    client.status = request.form.get('rdv_status')
    client.rdv_type = request.form.get('rdv_type')
    try:
        db.session.commit()
        flash('Client modifié avec succès.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erreur lors de la modification : {str(e)}', 'danger')
    return redirect(url_for('client.clients'))

@client_bp.route('/clients/add', methods=['POST'])
def add_client():
    from flask import request, redirect, url_for, flash
    last_name = request.form.get('last_name')
    first_name = request.form.get('first_name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    address = request.form.get('address')
    rdv_status = request.form.get('rdv_status')
    rdv_type = request.form.get('rdv_type')
    if not last_name or not first_name or not email:
        flash('Nom, prénom et email sont obligatoires.', 'danger')
        return redirect(url_for('client.clients'))
    try:
        new_client = Client(
            last_name=last_name,
            first_name=first_name,
            email=email,
            phone=phone,
            address=address,
            status=rdv_status,
            rdv_type=rdv_type
        )
        db.session.add(new_client)
        db.session.commit()
        flash('Client ajouté avec succès.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erreur lors de l\'ajout : {str(e)}', 'danger')
    return redirect(url_for('client.clients'))
