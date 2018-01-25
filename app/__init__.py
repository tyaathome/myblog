from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
csrf = CSRFProtect(app)

from app.user.user import user
app.register_blueprint(user, url_prefix = '/user')

from app import models

@app.route('/')
def index():
    return render_template('index.html')