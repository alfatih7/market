from flask import Flask, abort, redirect, jsonify, render_template, url_for, request
# import market.views
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,  SubmitField, BooleanField, SelectField, validators, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from setup import setup_db, Category, Item, db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from forms import CategoryForm, ItemForm
from flask_cors import CORS, cross_origin


def create_app(test_config=None):
    # create and configure the app

    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'b0c12fbf9a91b99f4acf8a57e4b2ad2f'
    setup_db(app)
    CORS(app)

    ##########################################################
    # create session
    dbpath = "postgres://{}:{}@{}/{}".format(
        'postgres', '*******', 'localhost:5432', 'marketdb')
    engine = create_engine(dbpath, echo=True)
    Base = declarative_base()
    Session = sessionmaker(bind=engine)
    session = Session()

    @ app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    # GLOBAL QUERY
    cat_qery = Category.query.all()
    # category_name = SelectField('category name', validators=[
    #     DataRequired(), Length(min=3, max=30)], choices=[(c.id, c.type)for c in cat_qery])
    # name = StringField('item name', validators=[
    #     DataRequired(), Length(min=3, max=30)])
    # origin_price = IntegerField('origin price', validators=[
    #     DataRequired(), Length(min=3, max=30)])
    # sale_price = IntegerField('sale price', validators=[
    #     DataRequired(), Length(min=3, max=30)])
    # count = IntegerField('number of items', validators=[
    #     DataRequired(), Length(min=3, max=30)])
    # submit = SubmitField('Add item')

    @ app.route('/home')
    def home():
        return render_template('pages/home.html')

    @ app.route('/categories')
    def get_all_categories():
        cat_qerys = session.query(Category).join(Item).all()
        categories = [v.format() for v in cat_qerys]

        return render_template('pages/categories.html', title='Category', categories=categories)

    @ app.route('/create/category')
    def get_category():
        form = CategoryForm()
        return render_template('/forms/new_category.html', title='Category', form=form)

    @ app.route('/create/category', methods=['POST'])
    def create_category():
        type = request.form.get('categoryType', '')
        new_category = Category(type=type)
        new_category.insert()
        return redirect(url_for('home'))

    @ app.route('/categories/<int:id>')
    def method_name(id):
        category = Category.query.get(id).format()
        return render_template('/layouts/category_layout.html', category=category)

    @ app.route('/edit/categories', methods=['GET', 'POST'])
    def edit_category():
        categories = [(name, item) for name, item in session.query(
            Category.type, Item.name).order_by(Category.id).join(Item)]

        # category = Category.query.join(Item).all()
        # # items = session.query(Category.id).all()
        # cat = session.query(Category.id, Category.type,
        #                     Category.item).outerjoin(Item)
        # items = session.query(Item).filter()
        # it = [i.name for i in items]
        # categories = [(c.id, c.type, c.name) for c in cat]
        # listItem = []

        # jsonify({
        #     'categories': [{c.id: c.type} for c in category]
        # })
        return render_template('/forms/edit_category.html',
                               title='Updat categories',
                               categories=categories
                               )

    @ app.route('/create/item')
    def get_item():
        category = Category.query.all()
        category_choice = [(c.id, c.type) for c in category]
        form = ItemForm(category_choice)
        return render_template('/forms/new_item.html', title='New item', form=form)

    @ app.route('/create/item', methods=['POST'])
    def create_item():
        error = False

        try:
            name = request.form.get('name', '')
            temp_category_name = request.form.get('category_name')
            new_category_name = ','.join(temp_category_name)
            new_origin_price = request.form.get('origin_price', '')
            new_sale_price = request.form.get('sale_price', '')
            new_count = request.form.get('count', '')
            category = Category.query.filter(
                Category.id == new_category_name[0]).one_or_none().format()
            id = category['id']
            new_item = Item(name=name, category_id=id,
                            origin_price=new_origin_price, sale_pric=new_sale_price, count=new_count)
            new_item.insert()
        except:
            error = True
        finally:
            return redirect(url_for('home'))
            # return jsonify({
            #     'error': error,
            #     'id': category['id']
            # })

    @app.route('/items')
    def get_all_items():
        item = session.query(Item).join(Category).all()
        items = [v.format() for v in item]
        return render_template("pages/items.html", items=items)

    return app
