from fastapi import APIRouter, Depends,HTTPException,BackgroundTasks
from auth.auth import create_access_token,verify_token
from sqlalchemy.orm import Session
from database.connection import SessionLocal
from schemas.user_schema import UserCreate,Login
from services.user_services import get_users, create_user,get_user_by_id,update_user,delete_user
from models.user_model import User
from utils.security import verify_password
from services.email_services import send_registration_email

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/login")
def login(user:Login,db:Session=Depends(get_db)):
    db_user=db.query(User).filter(User.email==user.email).first()

    if not db_user:
        raise HTTPException(status_code=401,detail="Invalid email")
    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401,detail="Invalid password")
    token = create_access_token({"user_id":db_user.id})

    return{
        "access_token":token,
        "token_type":"bearer",
        "userName":db_user.username

    }
@router.get("/")
def home():
    return {"API is Working"}
@router.get("/users")
def read_users(db: Session = Depends(get_db),current_user = Depends(verify_token)):
    return get_users(db)

@router.post("/users")
def add_user(user: UserCreate,background_tasks:BackgroundTasks, db: Session = Depends(get_db)):
    new_user = create_user(db, user)
    background_tasks.add_task(send_registration_email, user.email, user.username)
    return new_user

@router.get("/users/{id}")
def getUserById(id: int, db: Session = Depends(get_db)):
    return get_user_by_id(db,id)

@router.put("/users/{id}")
def update_user_api(id: int, user: UserCreate, db: Session = Depends(get_db)):
    return update_user(db, id, user)

@router.delete("/users/{id}")
def delete_user_api(id: int, db: Session = Depends(get_db)):
    return delete_user(db, id)