# This file is where data entry forms are created. Forms are placed on templates 
# and users fill them out.  Each form is an instance of a class. Forms are managed by the 
# Flask-WTForms library.

from flask_wtf import FlaskForm
import mongoengine.errors
from wtforms.validators import URL, Email, DataRequired, NumberRange
from wtforms.fields.html5 import URLField, DateField, IntegerRangeField, EmailField
from wtforms import StringField, SubmitField, TextAreaField, IntegerField, SelectField, FileField, RadioField
from wtforms_components import TimeField

class ProfileForm(FlaskForm):
    username = StringField('Username')
    fname = StringField('First Name', validators=[DataRequired()])
    lname = StringField('Last Name', validators=[DataRequired()]) 
    image = FileField("Image") 
    phonenum = IntegerField('Phone #',)
    about = TextAreaField('About:', validators=[])
    submit = SubmitField('Submit')

class ConsentForm(FlaskForm):
    adult_fname = StringField('First Name',validators=[DataRequired()])
    adult_lname = StringField('Last Name',validators=[DataRequired()])
    adult_email = EmailField('Email',validators=[Email()])
    consent = RadioField('Do you want your parents or teachers to see your schedule data/graph', choices=[(True,"True"),(False,"False")])
    submit = SubmitField('Submit')
    

class ScheduleForm(FlaskForm):
    rating = SelectField("Hangout rating:", choices=[(None,'n/a'),(1,1),(2,2),(3,3),(4,4),(5,5)])
    starttime = TimeField("Start Time")   
    endtime = TimeField("End Time")   
    feel = SelectField("Feeling:", choices=[(None,'---'),(1,1),(2,2),(3,3),(4,4),(5,5)], validators=[DataRequired()])
    schedule_date = DateField("Start Date:")
    wake_date = DateField("End Date:")
    minstoschedule = IntegerField("People Joining:", validators=[NumberRange(min=0,max=100, message="Enter 1-100")])
    submit = SubmitField("Submit")

class BlogForm(FlaskForm):
    subject = StringField('Subject', validators=[])
    content = TextAreaField('Blog', validators=[])
    tag = StringField('Tag', validators=[])
    
    
    
    submit = SubmitField('Blog')

class CommentForm(FlaskForm):
    content = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField('Comment')

class HangoutForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    streetAddress = StringField('Address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    zipcode = StringField('Zipcode',validators=[DataRequired()])
    rating = SelectField('Rating',choices=[("1","1"),("2","2"),("3","3"),("4","4"),("5","5")])
    activites = StringField('Activites to recommend:', validators=[DataRequired()])
    #groupRating = SelectField('Recommended Group Size:',choices=[("1","1"),("2","2"),("3","3"),("4","4"),("5","5+")])
    submit = SubmitField('Submit')