from flask import render_template, request, redirect, session, url_for

from app import app, db
from app.forms import LoginForm
from app.models import User


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST':
        message = None
        if form.validate():
            username = form.username.data
            user = User.query.filter_by(username = username).first()
            if user != None:
                session['username'] = username
                user.logincount += 1
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('home'))
            else:
                message = u'用户不存在'
        else:
            message = form.errors['username'][0]
            usernameMessage = form.errors['username'][0]
            passwordMessage = form.errors['password'][0]
            if usernameMessage:
                message = usernameMessage
            elif passwordMessage:
                message = passwordMessage
        return render_template('login.html', form = form, message = message)
    return render_template('login.html', form = form)