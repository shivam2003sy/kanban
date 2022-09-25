from app import db
from flask_login import UserMixin
import jwt
import time
#  User models with UserMixin : 4 functions  from  flask_login
class User(UserMixin, db.Model):
    id = db.Column(db.Integer,primary_key=True)
    user = db.Column(db.String(64),unique = True)
    email = db.Column(db.String(120),unique = True)
    password = db.Column(db.String(500))
    public_id = db.Column(db.String(50), unique=True)
    list = db.relationship('List', backref='User', lazy=True)
    # def __init__(self, user, email, password):
    #     self.user       = user
    #     self.password   = password
    #     self.email      = email
    def get_by_id(self, id):
        return User.query.filter_by(public_id=id).first()
    def __repr__(self):
        return str(self.id) + ' - ' + str(self.user)
    def save(self):
        # inject self into db session    
        db.session.add( self )
        # commit change and save the object
        db.session.commit()
        return self 
    def to_json(self):
        json_user = {
            'id': self.id,
            'user': self.user,
            'email': self.email,
        }
        return json_user
    def from_json(self, json_user):
        self.user = json_user.get('user')
        self.email = json_user.get('email')
        self.password = json_user.get('password')
        return self
    def verify_password(self, password):
        return self.password == password
    def get_by_username(self, username):
        return User.query.filter_by(user=username).first()
    def get_by_id ( self ,  id ) :
            return   User.query.filter_by( public_id = id ).first ( )
    def login(self, username, password):
        user = User.query.filter_by(user=username).first()
        if user and user.verify_password(password):
            return user.to_json()
        return None


class List(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique = True,nullable=False)
    description =  db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    card = db.relationship('Card', backref='List', lazy=True)
    def __repr__(self):
        return str(self.name) +" "+str(self.card)
    def to_json(self):
        json_list = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
        }
        return json_list
    def save(self):
        # inject self into db session    
        db.session.add( self )
        # commit change and save the object
        db.session.commit()
        return self
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self
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
    def to_json(self):
        json_card = {
            'Title': self.Title,
            'id': self.id,
            'Content': self.Content,
            'deadline': self.deadline,
            'list_id': self.list_id,
            'Completed': self.Completed,
            'create_time': self.create_time,
            'complete_time': self.complete_time,
            'last_update': self.last_update
        }
        return json_card
    def save(self):
        # inject self into db session    
        db.session.add( self )
        # commit change and save the object
        db.session.commit()
        return self
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self