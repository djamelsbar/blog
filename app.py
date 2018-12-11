
from flask import Flask, render_template, request, flash,url_for,redirect
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from forms import ArticleForm
import os

basedir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'admin.db')

app.config['SECRET_KEY'] = 'mysecret'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

migrate = Migrate(app, db)
admin = Admin(app)



class Category(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String)
	desc = db.Column(db.String)

class Article(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	titre = db.Column(db.String)
	cont = db.Column(db.String)
	category_id = db.Column(db.String, db.ForeignKey('category.id'), nullable=False)
	category = db.relationship('Category', backref=db.backref('articless', lazy=True))


admin.add_view(ModelView(Article, db.session))

admin.add_view(ModelView(Category,db.session))

@app.route('/affiche/')
def affiche():
	if request.method == 'GET':
		articles = Article.query.all()  # avoir tt les article
		return render_template('affiche.html', articles=articles)




@app.route('/add/', methods=['GET', 'POST'])
def add():

	form = ArticleForm()
	if request.method == 'POST':

		if form.validate() == True:

			article = Article()
			article.titre = form.titre.data
			article.cont = form.cont.data
			article.category = form.category.data
			db.session.add(article)

			db.session.commit()
			return redirect(url_for('affiche'))

	return render_template('add.html', form=form)

@app.route('/delete/<id>')
def delete(id):
	missing = Article.query.filter_by(id=id).first()
	db.session.delete(missing)
	db.session.commit()
	flash("votre mesage a ete bien suprimer")
	return  redirect(url_for('affiche'))


@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
	article = Article.query.filter_by(id=id).first()
	form = ArticleForm(obj=article)


	if request.method == 'POST':
		if form.validate() == True :
				article.titre = form.titre.data
				article.cont = form.cont.data
				article.category.name = form.category.data
				db.session.commit()
				return redirect(url_for('affiche'))

	return render_template('edit.html', form=form,article=article)



