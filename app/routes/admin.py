from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import User, Role
from app import db
from werkzeug.security import generate_password_hash

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/users')
def admin_users():
    users = User.query.order_by(User.name).all()
    roles = Role.query.order_by(Role.name).all()
    return render_template('admin_users.html', users=users, roles=roles)

@admin_bp.route('/admin/users', methods=['POST'])
def create_user():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    role_name = request.form['role']

    role = Role.query.filter_by(name=role_name).first()
    if not role:
        flash('Role not found', 'danger')
        return redirect(url_for('admin.admin_users'))

    user = User(
        name=name,
        email=email,
        password_hash=generate_password_hash(password),
        role_id=role.id,
        is_active=True
    )
    db.session.add(user)
    db.session.commit()
    flash('Utilisateur créé avec succès', 'success')
    return redirect(url_for('admin.admin_users'))

# CRUD utilisateur
@admin_bp.route('/admin/users/<int:user_id>')
def user_detail(user_id):
    user = User.query.get_or_404(user_id)
    roles = Role.query.order_by(Role.name).all()
    return render_template('user_detail.html', user=user, roles=roles)

@admin_bp.route('/admin/users/<int:user_id>/edit', methods=['GET', 'POST'])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    roles = Role.query.order_by(Role.name).all()
    if request.method == 'POST':
        user.name = request.form['name']
        user.email = request.form['email']
        role_name = request.form['role']
        role = Role.query.filter_by(name=role_name).first()
        if role:
            user.role_id = role.id
        password = request.form.get('password')
        if password:
            user.password_hash = generate_password_hash(password)
        db.session.commit()
        flash('Utilisateur modifié avec succès', 'success')
        return redirect(url_for('admin.admin_users'))
    return render_template('user_detail.html', user=user, roles=roles)

@admin_bp.route('/admin/users/<int:user_id>/toggle', methods=['POST'])
def toggle_user_active(user_id):
    user = User.query.get_or_404(user_id)
    user.is_active = not user.is_active
    if not user.is_active:
        # Assign 'user' role if deactivated
        user_role = Role.query.filter_by(name='user').first()
        user.role_id = user_role.id if user_role else user.role_id
    db.session.commit()
    flash('Statut utilisateur modifié', 'success')
    return redirect(url_for('admin.admin_users'))
