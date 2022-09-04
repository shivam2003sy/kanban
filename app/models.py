from app import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer,primary_key=True)
    user = db.Column(db.String(64),unique = True)
    email = db.Column(db.String(120),unique = True)
    password = db.Column(db.String(500))
    list = db.relationship('List', backref='User', lazy=True)
    def __init__(self, user, email, password):
        self.user       = user
        self.password   = password
        self.email      = email

    def __repr__(self):
        return str(self.id) + ' - ' + str(self.user)

    def save(self):
        # inject self into db session    
        db.session.add( self )
        # commit change and save the object
        db.session.commit()
        return self 

class List(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique = True,nullable=False)
    description =  db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    card = db.relationship('Card', backref='List', lazy=True)
    def __repr__(self):
        return str(self.name) +" "+str(self.card)
class Card(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    Title = db.Column(db.String(64),unique=True,nullable=False)
    Content = db.Column(db.String)
    deadline = db.Column(db.DateTime,nullable=False)
    list_id = db.Column(db.Integer, db.ForeignKey('list.id'),nullable=False)
    Completed = db.Column(db.Boolean,default=False)
    create_time = db.Column(db.DateTime,nullable=False)
    complete_time = db.Column(db.DateTime)
    last_update = db.Column(db.DateTime)
    def __repr__(self):
        return '<Card %r>' % self.Title

