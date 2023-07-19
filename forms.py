from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, Length


class AddCustomerForm(FlaskForm):
    """Form for adding Customers."""
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])
  
class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])
