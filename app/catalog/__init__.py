from app import db, app
from functools import wraps
from sqlalchemy import desc
from app.models import Category, Item, User
from app.forms import CategoryForm, ItemForm
from flask import Blueprint, render_template, g, request, redirect, url_for,\
    abort, session, flash

catalog = Blueprint('catalog', __name__)


# checking for existing of requested category
def check_category_exists(f):
    @wraps(f)
    def wrapper(*args, **kwds):
        category = db.session.query(Category).filter_by(
            name=kwds['category_name']).first()
        if not category:
            return abort(404)
        kwds['category'] = category
        return f(*args, **kwds)
    return wrapper


# checking user logged or not
def check_user_logged(f):
    @wraps(f)
    def wrapper(*args, **kwds):
        if not session.get('user_id'):
            flash('You need to signin first !!', 'warning')
            return redirect(url_for('index'))
        return f(*args, **kwds)
    return wrapper


# checking user permission
def check_item_owner(f):
    @wraps(f)
    def wrapper(*args, **kwds):
        if kwds['item'].user_id != session.get('user_id'):
            flash(
                'You cannot edit or delete this item, you\'re not it\'s owner',
                'warning')
            return redirect(
                url_for(
                    'catalog.viewItem',
                    category_name=kwds['item'].category.name,
                    item_name=kwds['item'].name))
        return f(*args, **kwds)
    return wrapper


# checking user permission
def check_category_owner(f):
    @wraps(f)
    def wrapper(*args, **kwds):
        if kwds['category'].user_id != session.get('user_id'):
            flash(
             'You cannt edit or delete this category, you\'re not it\'s owner',
             'warning')
            return redirect(
                url_for(
                    'catalog.viewCategory',
                    category_name=kwds['category'].name))
        return f(*args, **kwds)
    return wrapper


# checking for existing of requested item
def check_item_exists(f):
    @wraps(f)
    def wrapper(*args, **kwds):
        category = db.session.query(Category).filter_by(
            name=kwds['category_name']).first()
        if not category:
            return abort(404)
        item = db.session.query(Item).filter_by(
            category_id=category.id, name=kwds['item_name']).first()
        if not item:
            return abort(404)
        kwds['category'] = category
        kwds['item'] = item
        return f(*args, **kwds)
    return wrapper


# getting query of categories for side menu
@app.before_request
def categoryQuery():
    g.categories = db.session.query(Category).all()


@catalog.route('/')
def recentItems():
    items = db.session.query(Item).order_by(desc(Item.id)).limit(9).all()
    return render_template('recent_items.html', items=items)


@catalog.route('/create-category', methods=['GET', 'POST'])
@check_user_logged
def createCategory():
    category_form = CategoryForm()
    if request.method == 'POST' and category_form.validate_on_submit():
        category = Category(
            name=category_form.data['category_name'],
            user_id=session.get('user_id'))
        db.session.add(category)
        db.session.commit()
        flash('Category created successfully', 'success')
        return redirect(
            url_for('catalog.viewCategory', category_name=category.name))
    return render_template('create_category.html', category_form=category_form)


@catalog.route('/<category_name>')
@check_category_exists
def viewCategory(category_name, **kwds):
    category = kwds['category']
    items = db.session.query(Item).filter_by(category_id=category.id).all()
    return render_template('view_cat.html', items=items, category=category)


@catalog.route('/edit/<category_name>', methods=['GET', 'POST'])
@check_user_logged
@check_category_exists
@check_category_owner
def editCategory(category_name, **kwds):
    category = kwds['category']
    category_form = CategoryForm()
    if request.method == 'POST' and category_form.validate_on_submit():
        category.name = category_form.data['category_name']
        db.session.add(category)
        db.session.commit()
        flash('Category edited successfully', 'success')
        return redirect(
            url_for('catalog.viewCategory', category_name=category.name))
    category_form.category_name.data = category.name
    return render_template(
        'edit_category.html', category_form=category_form, category=category)


@catalog.route('/delete/<category_name>', methods=['GET', 'POST'])
@check_user_logged
@check_category_exists
@check_category_owner
def deleteCategory(category_name, **kwds):
    category = kwds['category']
    category_form = CategoryForm()
    category_form.category_name.data = category.name
    if request.method == 'POST' and category_form.validate_on_submit():
        for item in category.items:
            db.session.delete(item)
        db.session.delete(category)
        db.session.commit()
        flash('Category deleted successfully', 'success')
        return redirect(url_for('catalog.recentItems'))
    return render_template(
        'delete_category.html', category_form=category_form, category=category)


@catalog.route('/<category_name>/create', methods=['GET', 'POST'])
@check_user_logged
@check_category_exists
def createItem(category_name, **kwds):
    category = kwds['category']
    item_form = ItemForm()
    item_form.item_category.choices = [
        (cat.name, cat.name) for cat in db.session.query(Category).all()]
    if request.method == 'POST' and item_form.validate_on_submit():
        selected_category = db.session.query(Category).filter_by(
            name=item_form.data['item_category']).first()
        item = Item(
            name=item_form.data['item_name'],
            description=item_form.data['item_description'],
            category=selected_category,
            user_id=session.get('user_id'))
        db.session.add(item)
        db.session.commit()
        flash('Item created successfully', 'success')
        return redirect(
            url_for('catalog.viewCategory', category_name=item.category.name))
    item_form.item_category.data = category.name
    return render_template('create_item.html', item_form=item_form)


@catalog.route('/<category_name>/view/<item_name>')
@check_item_exists
def viewItem(category_name, item_name, **kwds):
    item = kwds['item']
    return render_template('view_item.html', item=item)


@catalog.route('/<category_name>/edit/<item_name>', methods=['GET', 'POST'])
@check_user_logged
@check_item_exists
@check_item_owner
def editItem(category_name, item_name, **kwds):
    category = kwds['category']
    item = kwds['item']
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
        flash('Item edited successfully', 'success')
        return redirect(url_for('catalog.viewItem',
                        category_name=item.category.name, item_name=item.name))
    item_form.item_name.data = item.name
    item_form.item_description.data = item.description
    item_form.item_category.data = category.name
    return render_template('edit_item.html', item_form=item_form, item=item)


@catalog.route('/<category_name>/delete/<item_name>', methods=['GET', 'POST'])
@check_user_logged
@check_item_exists
@check_item_owner
def deleteItem(category_name, item_name, **kwds):
    category = kwds['category']
    item = kwds['item']
    item_form = ItemForm()
    item_form.item_name.data = item.name
    item_form.item_category.data = category.name
    item_form.item_description.data = item.description
    item_form.item_category.choices = [
        (cat.name, cat.name) for cat in db.session.query(Category).all()]
    if request.method == 'POST' and item_form.validate_on_submit():
        db.session.delete(item)
        db.session.commit()
        flash('Item deleted successfully', 'success')
        return redirect(
            url_for('catalog.viewCategory', category_name=category.name))
    return render_template(
        'delete_item.html', item_form=item_form, item=item)
