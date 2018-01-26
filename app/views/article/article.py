import markdown
from flask import Blueprint, render_template, request, redirect, url_for, g, session
from markupsafe import Markup
from sqlalchemy import func
from wtforms import SubmitField

from app import db
from app.forms import ArticleForm
from app.models import Article

article = Blueprint('article', __name__,
                    template_folder='templates')

@article.route('/add_article', methods=['GET', 'POST'])
def add():
    form = ArticleForm(request.form)
    messages = []
    if request.method == 'POST':
        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data
            if form.commit.data:
                username = request.cookies.get('username')
                if not username:
                    return redirect(url_for('index'))
                id = db.session.query(func.max(Article.id)).scalar()
                if not id:
                    id = 0
                id += 1
                tag = 'test'
                article = Article(id=id, title=title, content=content, tag=tag)
                db.session.add(article)
                db.session.commit()
                return redirect(url_for('.get_user_article_by_id', user = username, id = id))
            elif form.preview.data:
                content = form.content.data
                text = Markup(markdown.markdown(content, ['extra']))
                session['content'] = content
                session['is_preview'] = True
                return render_template('/article/add_article.html', form=form, content=text)
            elif form.edit.data:
                session['is_preview'] = False
                content = session['content']
                form.content.data = content
                return render_template('/article/add_article.html', form=form)
        else:
            messages = [r for k, v in form.errors.items() for r in v]
    else:
        session['content'] = ''
        session['is_preview'] = False
    return render_template('/article/add_article.html', form=form)

@article.route('/<user>/<id>')
def get_user_article_by_id(user, id):
    art = Article.query.filter_by(id=id).first_or_404()
    return render_template('/article/article_detail.html', article = art)