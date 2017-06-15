from app import db, app
from sqlalchemy import desc
from app.models import Category, Item, User
from app.forms import CategoryForm, ItemForm
from flask import Blueprint, render_template, g, request, redirect, url_for

catalog = Blueprint('catalog', __name__)


@app.before_request
def dbQuery():
    g.categories = db.session.query(Category).all()


@catalog.route('/')
def recentItems():
    items = db.session.query(Item).order_by(desc(Item.id)).limit(9).all()
    return render_template('recent_items.html', items=items)


@catalog.route('/create-category', methods=['GET', 'POST'])
def createCategory():
    category_form = CategoryForm()
    if request.method == 'POST' and category_form.validate_on_submit():
        category = Category(name=category_form.data['category_name'])
        db.session.add(category)
        db.session.commit()
        return redirect(
            url_for('catalog.viewCategory', category_name=category.name))
    return render_template('create_category.html', category_form=category_form)


@catalog.route('/<category_name>')
def viewCategory(category_name):
    category = db.session.query(Category).filter_by(name=category_name).first()
    items = db.session.query(Item).filter_by(category_id=category.id).all()
    return render_template('view_cat.html', items=items, category=category)


@catalog.route('/edit/<category_name>', methods=['GET', 'POST'])
def editCategory(category_name):
    category_form = CategoryForm()
    category = db.session.query(Category).filter_by(name=category_name).first()
    if request.method == 'POST' and category_form.validate_on_submit():
        category.name = category_form.data['category_name']
        db.session.add(category)
        db.session.commit()
        return redirect(
            url_for('catalog.viewCategory', category_name=category.name))
    category_form.category_name.data = category.name
    return render_template(
        'edit_category.html', category_form=category_form, category=category)


@catalog.route('/delete/<category_name>', methods=['GET', 'POST'])
def deleteCategory(category_name):
    category_form = CategoryForm()
    category = db.session.query(Category).filter_by(name=category_name).first()
    category_form.category_name.data = category.name
    if request.method == 'POST' and category_form.validate_on_submit():
        for item in category.items:
            db.session.delete(item)
        db.session.delete(category)
        db.session.commit()
        return redirect(url_for('catalog.recentItems'))
    return render_template(
        'delete_category.html', category_form=category_form, category=category)


@catalog.route('/<category_name>/create', methods=['GET', 'POST'])
def createItem(category_name):
    category = db.session.query(Category).filter_by(name=category_name).first()
    item_form = ItemForm()
    item_form.item_category.choices = [
        (cat.name, cat.name) for cat in db.session.query(Category).all()]
    if request.method == 'POST' and item_form.validate_on_submit():
        selected_category = db.session.query(Category).filter_by(
            name=item_form.data['item_category']).first()
        item = Item(
            name=item_form.data['item_name'],
            description=item_form.data['item_description'],
            category=selected_category)
        db.session.add(item)
        db.session.commit()
        return redirect(
            url_for('catalog.viewCategory', category_name=item.category.name))
    item_form.item_category.data = category.name
    return render_template('create_item.html', item_form=item_form)


@catalog.route('/<category_name>/view/<item_name>')
def viewItem(category_name, item_name):
    category = db.session.query(Category).filter_by(name=category_name).first()
    item = db.session.query(Item).filter_by(
        category_id=category.id, name=item_name).first()
    return render_template('view_item.html', item=item)


@catalog.route('/<category_name>/edit/<item_name>', methods=['GET', 'POST'])
def editItem(category_name, item_name):
    category = db.session.query(Category).filter_by(name=category_name).first()
    item = db.session.query(Item).filter_by(name=item_name).first()
    item_form = ItemForm()
    item_form.item_category.choices = [
        (cat.name, cat.name) for cat in db.session.query(Category).all()]
    if request.method == 'POST' and item_form.validate_on_submit():
        selected_category = db.session.query(Category).filter_by(
            name=item_form.data['item_category']).first()
        item.name = item_form.data['item_name']
        item.description = item_form.data['item_description']
        item.category = selected_category
        db.session.commit()
        return redirect(url_for('catalog.viewItem',
                        category_name=item.category.name, item_name=item.name))
    item_form.item_name.data = item.name
    item_form.item_description.data = item.description
    item_form.item_category.data = category.name
    return render_template('edit_item.html', item_form=item_form, item=item)


@catalog.route('/<category_name>/delete/<item_name>', methods=['GET', 'POST'])
def deleteItem(category_name, item_name):
    category = db.session.query(Category).filter_by(name=category_name).first()
    item = db.session.query(Item).filter_by(name=item_name).first()
    item_form = ItemForm()
    item_form.item_name.data = item.name
    item_form.item_category.data = category.name
    item_form.item_description.data = item.description
    item_form.item_category.choices = [
        (cat.name, cat.name) for cat in db.session.query(Category).all()]
    if request.method == 'POST' and item_form.validate_on_submit():
        db.session.delete(item)
        db.session.commit()
        return redirect(
            url_for('catalog.viewCategory', category_name=category.name))
    print item_form.errors
    return render_template(
        'delete_item.html', item_form=item_form, item=item)
