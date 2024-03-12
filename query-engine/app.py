from datetime import datetime
from models.tables import User
from utils.database import Session


def write_to_db(name, email):
    session = Session()
    user = User(name=name, email=email)
    session.add(user)
    session.commit()
    user_id = user.id
    timestamp = int(datetime.now().timestamp() * 1000)  # Convert to milliseconds
    session.close()
    return user_id, timestamp


def read_from_db(user_id):
    session = Session()
    user = session.query(User).filter_by(id=user_id).first()
    session.close()
    if user:
        return {"id": user.id, "name": user.name, "email": user.email}
    return None


def update_in_db(user_id, name=None, email=None):
    session = Session()
    user = session.query(User).filter_by(id=user_id).first()
    if user:
        if name:
            user.name = name
        if email:
            user.email = email
        session.commit()
        timestamp = int(datetime.now().timestamp() * 1000)  # Convert to milliseconds
        user_data = {"id": user.id, "name": user.name, "email": user.email}
    session.close()


def delete_from_db(user_id):
    session = Session()
    user = session.query(User).filter_by(id=user_id).first()
    if user:
        session.delete(user)
        session.commit()
    session.close()
