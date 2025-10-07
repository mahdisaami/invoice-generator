from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, IntegerField, FieldList, FormField
from wtforms.validators import DataRequired, Email, Optional


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class EntityForm(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])
    qty = IntegerField('Quantity', validators=[DataRequired()])
    fee = IntegerField('Fee', validators=[DataRequired()])
    discount = IntegerField('Discount', validators=[Optional()])



class InvoiceForm(FlaskForm):
    number = StringField('Invoice Number', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    customer = StringField('Customer Name', validators=[DataRequired()])
    description = TextAreaField('Description')
    entities = FieldList(FormField(EntityForm), min_entries=2, max_entries=10)
    submit = SubmitField('Save Invoice')

