from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, name="email")
    password = db.Column(db.String(150))
    name = db.Column(db.String(150))