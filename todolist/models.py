from datetime import timezone
from flask_login import UserMixin
from sqlalchemy.sql import func 
from sqlalchemy import Column, Integer, String, ForeignKey
from . import db

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(1000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    image = db.Column(db.String(255)) 
    created = db.Column(db.DateTime, default=func.now())  # Thời gian tạo
    finished = db.Column(db.DateTime, nullable=True)  # Thời gian hoàn thành
    is_finished = db.Column(db.Boolean, default=False)  # Trạng thái hoàn thành
    due_date = db.Column(db.DateTime, nullable=True)  # Thời hạn hoàn thành

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    user_name = db.Column(db.String(150), unique=True, nullable=False)
    notes = db.relationship("Note", backref="user", lazy=True)
    is_blocked = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    avatar = db.Column(db.String(255), default="default.png")
    

    def __init__(self, email, password, user_name, is_blocked=False, is_admin=False):
        self.email = email
        self.password = password
        self.user_name = user_name
        self.is_blocked = is_blocked
        self.is_admin = is_admin 
