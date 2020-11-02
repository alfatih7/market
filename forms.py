from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,  SubmitField, BooleanField, SelectField, validators, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from setup import setup_db, Category, Item, db
import market


# cat = Category.query.all()
# chocesList = [c.format() for c in cat]


# def choic_quer():
#     return Category.query


class CategoryForm(FlaskForm):
    categoryType = StringField('Category type', validators=[
                               DataRequired(), Length(min=5, max=30)])
    submit = SubmitField('Add category')


class ItemForm(FlaskForm):
    name = StringField('item name', validators=[
        DataRequired(), Length(min=3, max=30)])
    category_name = SelectField('category name', validators=[
        DataRequired()], choices=[])
    origin_price = IntegerField('origin price', validators=[
        DataRequired(), Length(min=3, max=30)])
    sale_price = IntegerField('sale price', validators=[
        DataRequired(), Length(min=3, max=30)])
    count = IntegerField('number of items', validators=[
        DataRequired(), Length(min=3, max=30)])
    submit = SubmitField('Add item')

    def __init__(self, selection_choice):
        super(ItemForm, self).__init__()
        self.category_name.choices = selection_choice

    # def __init__(self, name, category_name, origin_price, sale_price, count, submit):
    #     self.category_name = category_name
    #     self.name = name
    #     self.origin_price = origin_price
    #     self.sale_price = sale_price
    #     self.count = count
    #     self.submit = submit
