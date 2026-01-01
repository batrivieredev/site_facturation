import os
import sys
import subprocess

venv_path = os.path.join(os.getcwd(), 'venv')
activate_script = os.path.join(venv_path, 'bin', 'activate_this.py')
pip_path = os.path.join(venv_path, 'bin', 'pip')
python_path = os.path.join(venv_path, 'bin', 'python')

# Create venv if missing
if not os.path.isdir(venv_path):
    print('Creating virtual environment...')
    subprocess.run([sys.executable, '-m', 'venv', 'venv'])
    print('Virtual environment created.')

# Install requirements if Flask not available
try:
    import flask
except ImportError:
    print('Installing requirements in venv...')
    subprocess.run([pip_path, 'install', '--break-system-packages', '-r', 'requirements.txt'])

# Relaunch script in venv if not already
if sys.executable != python_path:
    print('Restarting in venv...')
    os.execv(python_path, [python_path] + sys.argv)

# --- FLASK APP LAUNCH ---
from app import create_app, db
from app.models.user import User, Role
from flask_migrate import upgrade

app = create_app()

def setup_database_and_admin(app):
    with app.app_context():
        upgrade()
        # Only create admin after migrations
        try:
            admin_role = Role.query.filter_by(name='admin').first()
        except Exception:
            print("Database tables do not exist yet. Skipping admin creation.")
            return
        if not admin_role:
            admin_role = Role(name='admin')
            db.session.add(admin_role)
            db.session.commit()
        admin_email = os.environ.get('ADMIN_EMAIL', 'admin@local.com')
        admin_password = os.environ.get('ADMIN_PASSWORD', 'admin123')
        admin_user = User.query.filter_by(email=admin_email).first()
        if not admin_user:
            from app.services.auth_service import hash_password
            admin_user = User(
                name='Admin',
                email=admin_email,
                password_hash=hash_password(admin_password),
                role_id=admin_role.id,
                is_active=True
            )
            db.session.add(admin_user)
            db.session.commit()

if __name__ == "__main__":
    setup_database_and_admin(app)
    app.run(debug=True)
