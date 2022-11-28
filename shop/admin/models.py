from shop import db
from datetime import datetime
#links to the main database to create a new table  

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50),unique=False, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(180),unique=False, nullable=False)
    profile = db.Column(db.String(180), unique=False, nullable=False,default='profile.jpg')
    #flaskwtf validates the profile image upload

    def __repr__(self):
        return '<User %r>' % self.username
#creates a table 'User' with column names of id, name, username, email, password, profile to store information 



db.create_all()
#creates the table within the database that ius connected 