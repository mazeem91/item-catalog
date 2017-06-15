from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length


class CategoryForm(FlaskForm):
    category_name = StringField('Category name', validators=[
        DataRequired(message='Requiered!'),
        Length(max=128, message='Length is 128 characters max !')])


class ItemForm(FlaskForm):
    item_name = StringField('Item name', validators=[
        DataRequired(message='Requiered!'),
        Length(max=128, message='Length is 128 characters max !')])
    item_description = TextAreaField('Description', validators=[
        DataRequired(message='Requiered!')])
    item_category = SelectField('category')
