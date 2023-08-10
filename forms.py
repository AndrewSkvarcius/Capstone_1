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


class Add_Products(FlaskForm):
     product_name = StringField('Product Name', validators=[DataRequired()] )
     description = StringField("Description", validators=[Length(max=255)])
     image_url =  StringField("Image URL")
     quantity = SelectField('Quantity', choices=[(int(i), int(i)) for i in range(1, 11)],validators=[DataRequired()] )
     price = TextAreaField('Price')