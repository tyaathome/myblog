import time
from flask import render_template, request, redirect, session, url_for, Response, make_response, current_app, Blueprint
from sqlalchemy import func

from app import app, db
from app.forms import LoginForm, SignForm
from app.models import User


user = Blueprint('user', __name__,
                 template_folder='templates',
                 static_folder='static')

@user.route('/home')
def home():
    username = request.cookies.get('username')
    return render_template('/user/home.html', username = username)

@user.route('/login', methods = ['GET', 'POST'])
def login():
    if checkLogin():
        return redirect(url_for('.home'))
    else:
        form = LoginForm(request.form)
        if request.method == 'POST':
            messages = []
            if form.validate():
                username = form.username.data
                password = form.password.data
                user = User.query.filter_by(username = username).first()
                if user != None and user.password == password:
                    user.logincount += 1
                    db.session.add(user)
                    db.session.commit()
                    response = make_response(redirect(url_for('.home')))
                    response.set_cookie('username',value=username, expires=time.time()+24*60*60)
                    return response
                else:
                    messages.append('账号或密码错误')
            else:
                messages = [r for k, v in form.errors.items() for r in v]
            return render_template('/user/login.html', form = form, messages = messages)
        return render_template('/user/login.html', form = form)

def checkLogin():
    username = request.cookies.get('username')
    if username:
        return True
    else:
        return False

@user.route('/sign', methods=['GET', 'POST'])
def sign():
    form = SignForm(request.form)
    if request.method == 'POST':
        messages = []
        if form.validate():
            username = form.username.data
            email = form.email.data
            password = form.password.data
            user = User.query.filter_by(username = username).first()
            user2 = User.query.filter_by(email = email).first()
            if user or user2 :
                if user:
                    messages.append('该用户已存在')
                if user2:
                    messages.append('该邮箱已存在')
                return render_template('/user/sign.html', form = form, messages = messages)
            id = db.session.query(func.max(User.id)).scalar()
            if not id:
                id = 0
            id += 1
            user = User(id = id, username = username, email = email, password = password, logincount = 0)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('.login'))
        else:
            messages = [r for k, v in form.errors.items() for r in v]
        return render_template('/user/sign.html', form = form, messages = messages)
    return render_template('/user/sign.html', form = form)

@user.route('/logout', methods=['GET', 'POST'])
def logout():
    response = make_response(redirect(url_for('index')))
    response.set_cookie('username', value='', expires=0)
    return response