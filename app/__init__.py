from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
csrf = CSRFProtect(app)
from flaskext.markdown import Markdown

md = Markdown(app)

from app.views.user.user import user
from app.views.article.article import article
app.register_blueprint(user, url_prefix = '/user')
app.register_blueprint(article, url_prefix = '/article')

from app import models

@app.route('/')
def index():
    return render_template('index.html')