from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, DateField, TextAreaField, RadioField
from wtforms.validators import DataRequired,Email,EqualTo, length
from wtforms import ValidationError
from flask_wtf.file import FileField, FileAllowed
from flask import flash



class Postform(FlaskForm):
    title = StringField('title', validators=(DataRequired(), length(max=100), ))
    post = TextAreaField('post', validators=(DataRequired(), length(max=200), ))
    # date = DateField('Date', format='%Y-%m-%d', validators=(DataRequired(),))
    submit = SubmitField('submit posts')

class Commentform(FlaskForm):
    anonymous = RadioField('anonymous ', choices=[(False,'Unanonymous'),(True,'Anonymous')], default=False)
    comment = TextAreaField('post', validators=(DataRequired(), length(max=200), ))
    submit = SubmitField('submit conmment')

class Likeform(FlaskForm):
    like = SelectField(u'like', choices=[('1', 'like'), ('0', 'dislike')], validators=(DataRequired(),))
    submit = SubmitField('submit')