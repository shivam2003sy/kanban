# from flask  import json, url_for, jsonify, render_template
# from jinja2  import TemplateNotFound
# from app import app
# from . models import User
# from app   import app,db
# from . common import *
# from sqlalchemy import desc,or_
# import hashlib
# from flask_mail  import Message
# import re
# from flask import render_template
# from models import User , List , Card
# import os, datetime, time, random
# import matplotlib.pyplot as plt
# from models import Card
# # build a Json response
# def response( data ):
#     return app.response_class( response=json.dumps(data),
#                                status=200,
#                                mimetype='application/json' )
# def g_db_commit( ):
#     db.session.commit( );    

# def g_db_add( obj ):
#     if obj:
#         db.session.add ( obj )

# def g_db_del( obj ):
#     if obj:
#         db.session.delete ( obj )

from flask import current_app
from functools import wraps
import jwt
from flask import request, abort
from flask import current_app
from app import app
from app.models import *

def token_required(f):
    (f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
        if not token:
            return {
                "message": "Authentication Token is missing!",
                "data": None,
                "error": "Unauthorized"
            }, 401
        try:
            data=jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
            current_user = User.query.filter_by(id=data['id']).first()
            app.logger.error(current_user.id)
            if current_user.id != data['id']:
                return {
                "message": "Invalid Authentication token!",
                "data": None,
                "error": "Unauthorized"
            }, 401
            # if not current_user["active"]:
            #     abort(403)
        except Exception as e:
            return {
                "message": "Something went wrong",
                "data": None,
                "error": str(e)
            }, 500
        return f(current_user, *args, **kwargs)
    return decorated

