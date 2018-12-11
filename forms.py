from flask_wtf import FlaskForm
from wtforms import  TextAreaField, SubmitField,  StringField
from wtforms import validators
from wtforms.ext.sqlalchemy.fields import QuerySelectField



def get_category():
    from app import Category
    return Category.query.all()



class ArticleForm(FlaskForm):
    titre = StringField("Name Of title", [validators.DataRequired("Please enter title.")])
    cont = TextAreaField("cont", [validators.DataRequired("Please enter title.")])
    category = QuerySelectField('Category', [validators.DataRequired(u'Please select a Category')],query_factory=get_category, get_label='name', allow_blank=True)
    submit = SubmitField("Submit")



