from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, DateField, TextAreaField, RadioField
from wtforms.validators import DataRequired,Email,EqualTo, length
from wtforms import ValidationError
from flask_wtf.file import FileField, FileAllowed
from flask import flash



class Postform(FlaskForm):
    title = StringField('title', validators=(DataRequired(), length(max=100), ))
    post = TextAreaField('post', validators=(DataRequired(), length(max=200), ))
    submit = SubmitField('submit posts')

class DeletePostForm(FlaskForm):
    submit = SubmitField('Delete')
class Commentform(FlaskForm):
    anonymous = RadioField('anonymous ', choices=[('Unanonymous','Unanonymous'),('Anonymous','Anonymous')], default='Unanonymous')
    comment = TextAreaField('post', validators=(DataRequired(), length(max=200), ))
    submit = SubmitField('submit conmment')

class DeleteEventForm(FlaskForm):
    submit = SubmitField('Delete')

class qaform(FlaskForm):
    title = StringField('title', validators=(DataRequired(), length(max=100),))
    content = TextAreaField('content', validators=(DataRequired(), length(max=200),))
    submit = SubmitField('submit QA')

