from app import db, app
from sqlalchemy import desc
from app.forms import CategoryForm
from app.models import Category, Item, User
from flask import Blueprint, render_template, g, request

catalog = Blueprint('catalog', __name__)


@app.before_request
def dbQuery():
    g.categories = db.session.query(Category).all()


@catalog.route('/')
def recentItems():
    items = db.session.query(Item).order_by(desc(Item.id)).limit(9).all()
    return render_template('recent_items.html', items=items)


@catalog.route('/create', methods=['GET', 'POST'])
def createCategory():
    category_form = CategoryForm()
    if request.method == 'POST' and category_form.validate_on_submit():
        print ok
    if category_form.category_name.errors:
        print 'fff'
    return render_template('create_category.html', category_form=category_form)


@catalog.route('/<category_name>')
def viewCategory(category_name):
    category = db.session.query(Category).filter_by(name=category_name).first()
    items = db.session.query(Item).filter_by(category_id=category.id).all()
    return render_template('view_cat.html', items=items)


@catalog.route('/edit/<category>')
def editCategory(category):
    return 'edited category'


@catalog.route('/delete/<category>')
def deleteCategory(category):
    return 'deleted category'


@catalog.route('/<category_name>/create', methods=['GET', 'POST'])
def createItem(category_name):
    return 'created item'


@catalog.route('/<category_name>/view/<item_name>')
def viewItem(category_name, item_name):
    category = db.session.query(Category).filter_by(name=category_name).first()
    item = db.session.query(Item).filter_by(
        category_id=category.id, name=item_name).first()
    return render_template('view_item.html', item=item)


@catalog.route('/<category_name>/edit/<item_name>')
def editItem(category_name, item_name):
    return 'edited item'


@catalog.route('/<category_name>/delete/<item_name>')
def deleteItem(category_name, item_name):
    return 'deleted item'
