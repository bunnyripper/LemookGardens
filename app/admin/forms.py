from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed,FileRequired
from wtforms import StringField,PasswordField,TextAreaField,BooleanField
from wtforms.validators import DataRequired,Optional

class LoginForm(FlaskForm):
    username=StringField("Username",validators=[DataRequired()])
    password=PasswordField("password",validators=[DataRequired()])

class AnnouncementForm(FlaskForm):
    title=StringField("Title",validators=[DataRequired()])
    content=TextAreaField("Content",validators=[DataRequired()])
    image=FileField("Image (optional)",validators=[
        Optional(),
        FileAllowed(["jpg","jpeg","png","gif","webp"],"Images only")
        ])
    is_active=BooleanField("Active",default=True)