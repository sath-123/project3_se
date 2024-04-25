# application/frontend/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, HiddenField, IntegerField, DecimalField
from wtforms.validators import DataRequired, Email, Optional, NumberRange


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    first_name = StringField('First name', validators=[DataRequired()])
    last_name = StringField('Last name', validators=[DataRequired()])
    email = StringField('Email address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')

class AddProductForm(FlaskForm):
    name=StringField('name', validators=[DataRequired()])
    slug=StringField('slug', validators=[DataRequired()])
    price=IntegerField('price',validators=[DataRequired()])
    submit = SubmitField('Add Product')

class OrderItemForm(FlaskForm):
    product_id = HiddenField(validators=[DataRequired()])
    quantity = IntegerField(validators=[DataRequired()])
    order_id = HiddenField()
    submit = SubmitField('Update')

class SearchForm(FlaskForm):
    vendor_id = IntegerField('vendor_id')
    submit = SubmitField('Search')
    

class ItemForm(FlaskForm):
    product_id = HiddenField(validators=[DataRequired()])
    quantity = HiddenField(validators=[DataRequired()], default=1)

class ItemForm2(FlaskForm):
    product_id = HiddenField(validators=[DataRequired()])
    quantity = HiddenField(validators=[DataRequired()], default=1)
    price = HiddenField(validators=[DataRequired()])
    
class ProductFilterForm(FlaskForm):
    vendor_id = IntegerField('Vendor ID', validators=[Optional()])
    min_price = DecimalField('Min Price', validators=[Optional(), NumberRange(min=0)])
    max_price = DecimalField('Max Price', validators=[Optional(), NumberRange(min=0)])
    submit = SubmitField('Filter')

class ChatForm(FlaskForm):
    question = StringField('question')
    submit = SubmitField('Ask')