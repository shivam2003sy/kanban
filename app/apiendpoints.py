from flask import Flask ,make_response
from flask import jsonify
from flask import request
from app import app ,db
from functools import wraps
import jwt
import uuid
import datetime
from app.models import User, List, Card
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message' : 'Token is missing!'}), 401
        try: 
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message' : 'Token is invalid!'}), 401
        return f(current_user, *args, **kwargs)
    return decorated



# @app.route('/api/user', methods=['GET'])
# # @token_required
# def get_all_users():
#     users = User.query.all()
#     output = []
#     for user in users:
#         user_data = {}
#         user_data['public_id'] = user.public_id
#         user_data['user'] = user.user
#         user_data['password'] = user.password
#         output.append(user_data)
#     return jsonify({'users' : output})

# @app.route('api/user/<public_id>', methods=['GET'])
# @token_required
# def get_one_user(current_user, public_id):
#     if not current_user:
#         return jsonify({'message' : 'Cannot perform that function!'})
#     user = User.query.filter_by(public_id=public_id).first()
#     if not user:
#         return jsonify({'message' : 'No user found!'})

#     user_data = {}
#     user_data['public_id'] = user.public_id
#     user_data['name'] = user.name
#     user_data['password'] = user.password
#     return jsonify({'user' : user_data})

@app.route('/api/user', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data or not data['username'] or not data['password']:
        return jsonify({'message' : 'Please provide name and password!'}) , 400
    new_user = User(public_id=str(uuid.uuid4()), user=data['username'], password=data["password"], )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message' : 'New user created!'}) , 201

# @app.route('/api/auth/user/delete', methods=['DELETE'])
# @token_required
# def delete_user(public_id):
#     user = User.query.filter_by(public_id=public_id).first()
#     if not user:
#         return jsonify({'message' : 'No user found!'})
#     db.session.delete(user)
#     db.session.commit()
#     return jsonify({'message' : 'The user has been deleted!'})

@app.route('/api/auth/login')
def apilogin():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})
    user = User.query.filter_by(user=auth.username).first()
    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})
    if (user.password == auth.password):
        token = jwt.encode({'public_id' : user.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
        return jsonify({'token' : token})
    return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

@app.route('/api/list' ,methods =['GET'])
@token_required
def get_all_lists(current_user):
    lists = List.query.all()
    output = []
    for list in lists:
        list_data = {}
        list_data['id'] = list.id
        list_data['name'] = list.name
        list_data['description'] = list.description
        output.append(list_data)
    return jsonify({'lists' : output})

# @app.route('/todo', methods=['GET'])
# @token_required
# def get_all_todos(current_user):
#     todos = Todo.query.filter_by(user_id=current_user.id).all()

#     output = []

#     for todo in todos:
#         todo_data = {}
#         todo_data['id'] = todo.id
#         todo_data['text'] = todo.text
#         todo_data['complete'] = todo.complete
#         output.append(todo_data)

#     return jsonify({'todos' : output})

# @app.route('/todo/<todo_id>', methods=['GET'])
# @token_required
# def get_one_todo(current_user, todo_id):
#     todo = Todo.query.filter_by(id=todo_id, user_id=current_user.id).first()

#     if not todo:
#         return jsonify({'message' : 'No todo found!'})

#     todo_data = {}
#     todo_data['id'] = todo.id
#     todo_data['text'] = todo.text
#     todo_data['complete'] = todo.complete

#     return jsonify(todo_data)

# @app.route('/todo', methods=['POST'])
# @token_required
# def create_todo(current_user):
#     data = request.get_json()

#     new_todo = Todo(text=data['text'], complete=False, user_id=current_user.id)
#     db.session.add(new_todo)
#     db.session.commit()

#     return jsonify({'message' : "Todo created!"})

# @app.route('/todo/<todo_id>', methods=['PUT'])
# @token_required
# def complete_todo(current_user, todo_id):
#     todo = Todo.query.filter_by(id=todo_id, user_id=current_user.id).first()

#     if not todo:
#         return jsonify({'message' : 'No todo found!'})

#     todo.complete = True
#     db.session.commit()

#     return jsonify({'message' : 'Todo item has been completed!'})

# @app.route('/todo/<todo_id>', methods=['DELETE'])
# @token_required
# def delete_todo(current_user, todo_id):
#     todo = Todo.query.filter_by(id=todo_id, user_id=current_user.id).first()

#     if not todo:
#         return jsonify({'message' : 'No todo found!'})

#     db.session.delete(todo)
#     db.session.commit()

#     return jsonify({'message' : 'Todo item deleted!'})