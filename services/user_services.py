from models.user_model import User
from fastapi import HTTPException
from utils.security import hash_password
from services.email_services import send_registration_email

def get_users(db):
    return db.query(User).order_by(User.id).all()

def create_user(db, user):
    hashed_password = hash_password(user.password)
    new_user = User(username=user.username,password=hashed_password,email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user_by_id(db, id):
    user= db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def update_user(db, id, user):
    hashed_password = hash_password(user.password)
    existing_user = db.query(User).filter(User.id == id).first()

    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    existing_user.username = user.username
    existing_user.password = hashed_password
    existing_user.email = user.email

    db.commit()
    db.refresh(existing_user)

    return existing_user

def delete_user(db, id):
    user = db.query(User).filter(User.id == id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()

    return {"message": "User deleted successfully"}