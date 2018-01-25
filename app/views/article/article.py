import markdown
from flask import Blueprint, render_template, request, redirect, url_for
from markupsafe import Markup
from sqlalchemy import func

from app import db
from app.forms import ArticleForm
from app.models import Article

article = Blueprint('article', __name__,
                    template_folder='templates')

@article.route('/add_article', methods=['GET', 'POST'])
def add():
    form = ArticleForm(request.form)
    messages = []
    if request.method == 'POST' and form.validate():
        username = request.cookies.get('username')
        if not username:
            return redirect(url_for('index'))
        id = db.session.query(func.max(Article.id)).scalar()
        if not id:
            id = 0
        id += 1
        title = form.title.data
        content = form.content.data
        tag = 'test'
        article = Article(id=id, title=title, content=content, tag=tag)
        db.session.add(article)
        db.session.commit()
        text = Markup(markdown.markdown(content, ['extra']))
        return render_template('/article/add_article.html', form=form, content=text)
    else:
        messages = [r for k, v in form.errors.items() for r in v]
    return render_template('/article/add_article.html', form = form)