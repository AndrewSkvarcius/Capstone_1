from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Length


class AddUserForm(FlaskForm):
    """Form for adding Customers."""
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])
  
class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])

class Order_Form(FlaskForm):
    quantity = SelectField('Quantity', choices=[(int(i), int(i)) for i in range(1, 11)],validators=[DataRequired()] )
    submit = SubmitField("Add To Order")
## Admin Forms  ##


class AdminLogin(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])

class AddAdminForm(FlaskForm):
    """Form for adding Customers."""
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])