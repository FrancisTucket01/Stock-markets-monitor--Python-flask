from ltwallet import db

class Users(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(100), unique = True)
    password = db.Column(db.String(100))
 
 
    def __init__(self, username, password):
        self.username = username
        self.password = password