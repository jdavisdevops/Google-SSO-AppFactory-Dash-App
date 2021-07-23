# from flaskapp.app import app
# from flask import current_app as app
from flaskapp import db

# from sqlalchemy.dialects.postgresql import JSON
# from flask_migrate import Migrate
# from pathlib import Path
# from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

# db = SQLAlchemy(app)
# migrate = Migrate(app, db)


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.String(30), primary_key=True)
    firstlast = db.Column(db.String(400), unique=False)
    first_name = db.Column(db.String(400), unique=False)
    last_name = db.Column(db.String(400), unique=False)
    email = db.Column(db.String(400), unique=False)
    profile_pic = db.Column(db.String(4000))

    def __init__(self, id, firstlast, first_name, last_name, email, profile_pic):
        self.id = id
        self.firstlast = firstlast
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.profile_pic = profile_pic

    def __repr__(self):
        return f"""
        <div> id: {self.id} </div>
        <div> firstlast: {self.firstlast} </div>
        <div> first_name: {self.first_name} </div>
        <div> last_name: {self.last_name} </div>
        <div> email: {self.email} </div>
        <div> profile_pic: {self.profile_pic} </div>
        
        """
