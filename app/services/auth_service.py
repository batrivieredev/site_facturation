from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User
from app import db

def hash_password(password):
    return generate_password_hash(password)

def verify_password(hash, password):
    return check_password_hash(hash, password)

def create_user(name, email, password, role_id):
    user = User(
        name=name,
        email=email,
        password_hash=hash_password(password),
        role_id=role_id,
        is_active=True
    )
    db.session.add(user)
    db.session.commit()
    return user

def authenticate_user(email, password):
    user = User.query.filter_by(email=email).first()
    if user and verify_password(user.password_hash, password):
        return user
    return None
