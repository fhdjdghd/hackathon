from sqlalchemy.orm import Session
from database import SessionLocal
from models import User

def check_user_exists(username: str, email: str) -> bool:
    db = SessionLocal()
    user = db.query(User).filter((User.username == username) | (User.email == email)).first()
    db.close()
    return user is not None