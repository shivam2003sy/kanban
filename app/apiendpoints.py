from app import api  ,app
from flask import request
from app import db
from  app.models import List, Card , User
from flask import jsonify
import uuid 
import jwt
import datetime
from functools import wraps

from flask_restful import Resource, reqparse


def token_required(f):  
    @wraps(f)  
    def decorator(*args, **kwargs):

       token = None 

       if 'x-access-tokens' in request.headers:  
          token = request.headers['x-access-tokens'] 


       if not token:  
          return jsonify({'message': 'a valid token is missing'})   


       try:  
          data = jwt.decode(token, app.config[SECRET_KEY]) 
          current_user = User.query.filter_by(public_id=data['public_id']).first()  
       except:  
          return jsonify({'message': 'token is invalid'})  


          return f(current_user, *args,  **kwargs)  
    return decorator 

class UserLogin(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user', type=str, required=True, help='Username cannot be blank!')
        parser.add_argument('password', type=str, required=True, help='Password cannot be blank!')
        data = parser.parse_args()
        user = User.query.filter_by(user=data['user']).first()
        if user and user.verify_password(data['password']):
            return {'message': 'Login successful!'
            } , 200
        return {'message': 'Invalid credentials!'} , 401


class List(Resource):
    @token_required
    def get(self ,id):
        if user.is_authenticated:
            lists = List.query.filter_by(id=user.id).all()
            return jsonify(lists=[list.serialize for list in lists])
        

    # def post(self):
    #     parser = reqparse.RequestParser()
    #     parser.add_argument('title', type=str, required=True, help='Title cannot be blank!')
    #     data = parser.parse_args()
    #     list = List(title=data['title'])
    #     db.session.add(list)
    #     db.session.commit()
    #     return {'message': 'List created!'} , 201

class UserResource(Resource):
    def get(self, user_id):
        user = User.query.get(user_id)
        if user:
            return user.to_json() , 200
        else:
            return {'error': 'User not found'}, 404
    # def put(self, user_id):
    #     user = User.query.get(user_id)
    #     if user:
    #         if request.json['username']:
    #             user.username = request.json['username']
    #     db.session.commit()
    #     return user.to_json()
    #     else:
    #         return {'error': 'User not found'}, 404

    def delete(self, user_id):
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return {'result': True}
        else:
            return {'error': 'User not found'}, 404

@app.route('/api/users')
def get_all_user():
    users = User.query.all()
    return jsonify([user.to_json() for user in users])
@app.route('/api/register',methods=['POST'])
def register_api():
    user = User.query.filter_by(user=request.json['user']).first()
    if user:
        return {'error': 'User already exists'}, 409
    else:
        user = User(user= request.json['user'],password=request.json['password'] ,email=request.json['email'])
        db.session.add(user)
        db.session.commit()
        return user.to_json(), 201



api.add_resource(UserResource,'/api/user/<int:user_id>')
api.add_resource(UserLogin,'/api/login')

