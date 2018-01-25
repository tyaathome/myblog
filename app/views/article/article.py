from flask import Blueprint, render_template, request

from app.forms import ArticleForm

article = Blueprint('article', __name__,
                    template_folder='templates')

@article.route('/add_article', methods=['GET', 'POST'])
def add():
    form = ArticleForm(request.form)
    return render_template('/article/add_article.html', form = form)