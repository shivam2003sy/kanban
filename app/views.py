# Python modules
import datetime
from itertools import count
# Flask modules
from flask import render_template, request, url_for, redirect, send_from_directory
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.exceptions import HTTPException, NotFound, abort
from jinja2 import TemplateNotFound
from flask_restful import Resource
# App modules
from app import app, lm, db, bc, api
from app.models import User, List, Card
from app.forms import LoginForm, RegisterForm
# provide login manager with load_user callback


import matplotlib.pyplot as plt

@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Logout user
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

# Register a new user


@app.route('/register', methods=['GET', 'POST'])
def register():
    # declare the Registration Form
    form = RegisterForm(request.form)
    msg = None
    success = False
    if request.method == 'GET':
        return render_template('accounts/register.html', form=form, msg=msg)
    # check if both http method is POST and form is valid on submit
    if form.validate_on_submit():
        # assign form data to variables
        username = request.form.get('username', '', type=str)
        password = request.form.get('password', '', type=str)
        email = request.form.get('email', '', type=str)
        # filter User out of database through username
        user = User.query.filter_by(user=username).first()
        # filter User out of database through username
        user_by_email = User.query.filter_by(email=email).first()
        if user or user_by_email:
            msg = 'Error: User exists!'
        else:
            # pw_hash = bc.generate_password_hash(password)
            user = User(username, email,password)
            user.save()
            msg = 'User created, please <a href="' + \
                url_for('login') + '">login</a>'
            success = True
    else:
        msg = 'Input error'
    return render_template('accounts/register.html', form=form, msg=msg, success=success)
# Authenticate user


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Declare the login form
    form = LoginForm(request.form)
    # Flask message injected into the page, in case of any errors
    msg = None
    # check if both http method is POST and form is valid on submit
    if form.validate_on_submit():
        # assign form data to variables
        username = request.form.get('username', '', type=str)
        password = request.form.get('password', '', type=str)
        # filter User out of database through username
        user = User.query.filter_by(user=username).first()
        if user:
            # if bc.check_password_hash(user.password, password):
            #     login_user(user)
            #     return redirect(url_for('index'))
            if user.password == password:
                login_user(user)
                return redirect(url_for('index'))
            else:
                msg = "Wrong password. Please try again."
        else:
            msg = "No user registerd with this usename "
    return render_template('accounts/login.html', form=form, msg=msg)

# App main route + generic routing
@app.route('/')
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    else:
        log_id = current_user.get_id()
        user = User.query.filter_by(id=log_id).first_or_404()
        display_list = user.list
        CurrentDate = datetime.datetime.now()
        return render_template('index.html', list=display_list , CurrentDate=CurrentDate)
# Add a new list
@app.route('/createlist', methods=['GET', 'POST'])
def createlist():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    else:
        if request.method == 'GET':
            return render_template('create/createList.html')
        if request.method == 'POST':
            log_id = current_user.get_id()
            name = request.form.get('list_name')
            description = request.form.get('description')
            list_todo = List(name=name, user_id=log_id,
                             description=description)
            db.session.add(list_todo)
            db.session.commit()
            return redirect(url_for('index'))
#  edit list titles


@app.route('/createlist/<int:list_id>', methods=['GET', 'POST'])
def updatelist(list_id):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    else:
        if request.method == 'GET':
            list_todo = List.query.filter_by(id=list_id).first_or_404()
            return render_template('create/editList.html', list=list_todo)
        if request.method == 'POST':
            log_id = current_user.get_id()
            name = request.form.get('list_name')
            description = request.form.get('description')
            list_todo = List.query.filter_by(id=list_id).first_or_404()
            try:
                if name:
                    list_todo.name = name
                else:
                    list_todo.name = list_todo.name
                if description:
                    list_todo.description = description
                else:
                    list_todo.description = list_todo.description
            finally:
                db.session.commit()
                return redirect(url_for('index'))
# Delete a list
@app.route('/createlist/<int:list_id>/delete', methods=['DELETE'])
def deletelist(list_id):
    # if not current_user.is_authenticated:
    #     return redirect(url_for('login'))
    # else:
    list_todo = List.query.filter_by(id=list_id).first_or_404()
    for card in list_todo.card:
        db.session.delete(card)
        db.session.commit()
    db.session.delete(list_todo)
    db.session.commit()
    return {'message': 'List deleted'}
# Add a new card


@app.route('/createcard', methods=['GET', 'POST'])
def createcard():
    log_id = current_user.get_id()
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    else:
        if request.method == 'GET':
            user = User.query.filter_by(id=log_id).first_or_404()
            list_item = user.list
            return render_template('card/createcard.html', list_item=list_item)
        if request.method == "POST":
            list_get = request.form.get('list')
            list_from_name = List.query.filter_by(
                user_id=log_id, name=list_get).first()
            list_id = list_from_name.id

            title = request.form.get('title')
            content = request.form.get('content')
            deadline = datetime.datetime.strptime(
                request.form.get('deadline'), '%Y-%m-%d')
            check = request.form.get("checkbox")
            if check:
                completed = True
            else:
                completed = False
            created_time = datetime.datetime.now()
            new_card = Card(Title=title, Content=content, deadline=deadline,
                            list_id=list_id, Completed=completed, create_time=created_time)
            db.session.add(new_card)
            db.session.commit()
            return redirect(url_for('index'))

# Edit a card
@app.route('/createcard/<int:card_id>', methods=['GET', 'POST'])
def editcard(card_id):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    else:
        if request.method == 'GET':
            log_id = current_user.get_id()
            card = Card.query.filter_by(id=card_id).first_or_404()
            user = User.query.filter_by(id=log_id).first_or_404()
            list_item = user.list
            return render_template('card/editcard.html', card=card ,list_item=list_item)
        if request.method == "POST":
            title = request.form.get('title')
            content = request.form.get('content')
            deadline = datetime.datetime.strptime(
                request.form.get('deadline'), '%Y-%m-%d')
            check = request.form.get("checkbox")
            name = request.form.get('list')
            if check:
                completed = True
            else:
                completed = False
            card = Card.query.filter_by(id=card_id).first_or_404()
            try:
                if title:
                    card.Title = title
                else:
                    card.Title = card.Title
                if content:
                    card.Content = content
                else:
                    card.Content = card.Content
                if deadline:
                    card.deadline = deadline
                else:
                    card.deadline = card.deadline
                if completed:
                    card.Completed = completed
                else:
                    card.Completed = card.Completed
                if name:
                    id_list=current_user.get_id()
                    list_from_name = List.query.filter_by(user_id=id_list, name=name).first()
                    list_id = list_from_name.id
                    card.list_id = list_id
                else:
                    card.list_id = card.list_id
            finally:
                db.session.commit()
                return redirect(url_for('index'))
# mark a card as completed
@app.route('/createcard/<int:card_id>/completed', methods=['Post'])
def completed(card_id):
    card = Card.query.filter_by(id=card_id).first_or_404()
    card.Completed = True
    card.complete_time =datetime.datetime.now()
    db.session.commit()
    return {'message': 'Card completed'}

# Delete a card
@app.route('/createcard/<int:card_id>/delete', methods=['DELETE'])
def deletecard(card_id):
    card = Card.query.filter_by(id=card_id).first_or_404()
    db.session.delete(card)
    db.session.commit()
    return redirect(url_for('index'))

# ALL task summary page 
@app.route('/summary')
def summary():
    log_id = current_user.get_id()
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    else:
        user = User.query.filter_by(id=log_id).first_or_404()
        list_item = user.list
        card_dict ={}
        for list in list_item:
            graphs_of_list(list.id)
            card_dict[list.id] = []
            completed =0
            fail = 0
            going = 0
            total = 0
            for cards in list.card:
                total +=1
                if cards.Completed == True:
                    completed +=1
                elif cards.Completed == False and cards.deadline < datetime.datetime.now():
                    fail +=1
                else:
                    going +=1
            card_dict[list.id].append(completed)
            card_dict[list.id].append(fail)
            card_dict[list.id].append(going)
            card_dict[list.id].append(total)
        return render_template('summary/main.html', list=list_item , card_dict=card_dict)



def graphs_of_list(list_id):
    cards = Card.query.filter_by(list_id=list_id).all()
    x = []
    y = []
    for card in cards:
        if card.Completed :
            date_time = card.complete_time.strftime("%m/%d/%Y")
            x.append(date_time)
            i = Card.query.filter_by(complete_time=date_time ,Completed=True).all()
            y.append(len(i))
            app.logger.info(x)
            app.logger.info(y)
    # creating the bar plot
    plt.bar(x,y, color ='maroon',
            width = 0.4)
    plt.xlabel("Dates")
    plt.ylabel("No. of tasks completed")
    plt.title("Tasks completed")
    plt.show()