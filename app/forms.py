from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length


class CategoryForm(FlaskForm):
    category_name = StringField('Category name', validators=[
        DataRequired(message='Name of cateory is requiered!'),
        Length(max=128, message='Length of category is 128 characters max !')])
