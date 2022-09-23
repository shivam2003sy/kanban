from flask  import json, url_for, jsonify, render_template
from jinja2  import TemplateNotFound
from app import app
from . models import User
from app   import app,db
from . common import *
from sqlalchemy import desc,or_
import hashlib
from flask_mail  import Message
import re
from flask import render_template
from models import User , List , Card
import os, datetime, time, random
import matplotlib.pyplot as plt
from models import Card
# build a Json response
def response( data ):
    return app.response_class( response=json.dumps(data),
                               status=200,
                               mimetype='application/json' )
def g_db_commit( ):
    db.session.commit( );    

def g_db_add( obj ):
    if obj:
        db.session.add ( obj )

def g_db_del( obj ):
    if obj:
        db.session.delete ( obj )


