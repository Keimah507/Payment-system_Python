from .app.models.user import User
from .app.app import app
from sqlalchemy import create_engine

with app.app_context():
    db.create_all()