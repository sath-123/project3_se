# application/frontend/views.py
import requests
from flask import render_template, session, redirect, url_for, flash, request
from flask_login import current_user
from . import forms, frontend_blueprint
from .. import login_manager
from .api.UserClient import UserClient
from .api.VendorClient import VendorClient
from .api.ProductClient import ProductClient
from .api.OrderClient import OrderClient
import logging
import sys
import openai

log = logging.getLogger(__name__)

@login_manager.user_loader
def load_user(user_id):
    return None

@frontend_blueprint.route('/home_user', methods=['GET'])
def home_user():
    vendor_id = request.args.get('vendor_id', None, type=int)
    min_price = request.args.get('min_price', None, type=float)
    max_price = request.args.get('max_price', None, type=float)
    if current_user.is_authenticated:
        session['order'] = OrderClient.get_order_from_session()

    try:
        products = ProductClient.get_products(vendor_id=vendor_id, min_price=min_price, max_price=max_price)
    except requests.exceptions.ConnectionError:
        products = {'results': []}

    return render_template('home_user/index.html', products=products)

@frontend_blueprint.route('/home_vendor', methods=['GET','POST'])
def home_vendor():
    if current_user.is_authenticated:
        session['order'] = OrderClient.get_order_from_session()
    try:
        products = ProductClient.get_products()
    except requests.exceptions.ConnectionError:
        products = {'results': []}
    return render_template('home_vendor/index.html', products=products)
@frontend_blueprint.route('/chat', methods=['POST','GET'])
def chat():
    form = forms.ChatForm()
    print("enterde chat", file = sys.stderr)
    if request.method == "POST":
        
        api_key = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
        client = openai.OpenAI(api_key=api_key)
        question=form.question.data
        print(question, file =sys.stderr)
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                                    {"role": "system", "content": "You are a helpful assistant."},
                                    {"role": "user", "content": question}
                                ],
                )
       
            print(response ,file = sys.stderr)
            answer = response.choices[0].message.content.strip()
            print(answer, file=sys.stderr)
            # Return the answer in a JSON response
            return render_template('chat/index.html', form=form,answer=answer)
        except Exception as e:
            print(e , file=sys.stderr)
            flash('error')
    return render_template('chat/index.html', form=form,answer="")

@frontend_blueprint.route('/', methods=['GET'])
def home():
    return render_template('user_vendor_selection/index.html')

@frontend_blueprint.route('/register_user', methods=['GET', 'POST'])
def register_user():
    form = forms.RegistrationForm(request.form)
    if request.method == "POST" and form.validate_on_submit():
        username = form.username.data
        if UserClient.does_exist(username):
            flash('Please try another username', 'error')
            return render_template('register/index.html', form=form)
        else:
            user = UserClient.post_user_create(form)
            if user:
                flash('Thanks for registering, please login', 'success')
                return redirect(url_for('frontend.login_user'))
    else:
        flash('Errors found', 'error')
    return render_template('register/index.html', form=form)

@frontend_blueprint.route('/register_vendor', methods=['GET', 'POST'])
def register_vendor():
    form = forms.RegistrationForm(request.form)
    if request.method == "POST" and form.validate_on_submit():
        username = form.username.data
        if VendorClient.does_exist(username):
            flash('Please try another username', 'error')
            return render_template('register/index.html', form=form)
        else:
            vendor = VendorClient.post_vendor_create(form)
            if vendor:
                flash('Thanks for registering, please login', 'success')
                return redirect(url_for('frontend.login_vendor'))
    else:
        flash('Errors found', 'error')
    return render_template('register/index_vendor.html', form=form)

@frontend_blueprint.route('/login_user', methods=['GET', 'POST'])
def login_user():
    if current_user.is_authenticated:
        return redirect(url_for('frontend.home_user'))
    form = forms.LoginForm()
    if request.method == "POST" and form.validate_on_submit():
        api_key = UserClient.post_login(form)
        if api_key:
            session['user_api_key'] = api_key
            user = UserClient.get_user()
            session['user'] = user['result']
            order = OrderClient.get_order()
            if order.get('result', False):
                session['order'] = order['result']
            flash('Welcome back, ' + user['result']['username'], 'success')
            return redirect(url_for('frontend.home_user'))
        else:
            flash('Cannot login', 'error')
    else:
        flash('Errors found', 'error')
    return render_template('login/index.html', form=form)

@frontend_blueprint.route('/login_vendor', methods=['GET', 'POST'])
def login_vendor():
    if current_user.is_authenticated:
        return redirect(url_for('frontend.home_vendor'))
    form = forms.LoginForm()
    if request.method == "POST" and form.validate_on_submit():
        api_key = VendorClient.post_login(form)
        if api_key:
            session['user_api_key'] = api_key
            user = VendorClient.get_user()
            session['user'] = user['result']
            flash('Welcome back, ' + user['result']['username'], 'success')
            return redirect(url_for('frontend.home_vendor'))
        else:
            flash('Cannot login', 'error')
    else:
        flash('Errors found', 'error')
    return render_template('login/index_vendor.html', form=form)

@frontend_blueprint.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return render_template('user_vendor_selection/index.html')

@frontend_blueprint.route('/add', methods=['POST','GET'])
def add():
    form = forms.AddProductForm()
    if request.method == "POST" and form.validate_on_submit():
        product = ProductClient.create_product(form, session['user']['id'])
        if product:
            flash('Product added successfully', 'success')
            return redirect(url_for('frontend.home_vendor'))
        else:
            flash('Failed to add product', 'error')
    return render_template('add/index.html', form=form)

@frontend_blueprint.route('/product/<slug>', methods=['GET', 'POST'])
def product(slug):
    response = ProductClient.get_product(slug)
    item = response['result']
    form = forms.ItemForm2(product_id=item['id'], price=item['price'])
    if request.method == "POST":
        if 'user' not in session:
            flash('Please login', 'error')
            return redirect(url_for('frontend.login'))
        order = OrderClient.post_add_to_cart(product_id=item['id'], qty=1)
        session['order'] = order['result']
        flash('Order has been updated', 'success')
    return render_template('product/index.html', product=item, form=form)

@frontend_blueprint.route('/checkout', methods=['GET'])
def summary():
    if 'user' not in session:
        flash('Please login', 'error')
        return redirect(url_for('frontend.login'))

    if 'order' not in session:
        flash('No order found', 'error')
        return redirect(url_for('frontend.home'))
    
    order = OrderClient.get_order()

    if len(order['result']['items']) == 0:
        flash('No order found', 'error')
        return redirect(url_for('frontend.home'))

    return redirect(url_for('frontend.cart'))

@frontend_blueprint.route('/order/thank-you', methods=['GET'])
def thank_you():
    if 'user' not in session:
        flash('Please login', 'error')
        return redirect(url_for('frontend.login'))

    if 'order' not in session:
        flash('No order found', 'error')
        return redirect(url_for('frontend.home'))

    session.pop('order', None)
    flash('Thank you for your order', 'success')

    return render_template('order/thankyou.html')

@frontend_blueprint.route('/order/cart', methods=['GET', 'POST' ])
def cart():
    order = OrderClient.get_order()
    if 'user' not in session:
        flash('Please login', 'error')
        return redirect(url_for('frontend.login'))
    if 'order' not in session:
        flash('No order found', 'error')
        return redirect(url_for('frontend.home'))
    
    if len(order['result']['items']) == 0:
        flash('No order found', 'error')
        return redirect(url_for('frontend.home'))

    if request.method == 'POST':
        product_id = request.form.get('product_id')
        action = request.form.get('action')
        if action == 'increase_quantity':
            response = OrderClient.add_item(product_id,  1)
            if not response:
                flash('Failed to increase quantity.', 'error')
        elif action == 'decrease_quantity':
            response = OrderClient.remove_item(product_id, 1)
            if not response:
                flash('Failed to decrease quantity.', 'error')
        elif action == 'confirm_order':
            response = OrderClient.post_checkout()
            if not response:
                flash('Failed to checkout.', 'error')
            return redirect(url_for('frontend.thank_you'))

    order_response = OrderClient.get_order()
    if not order_response or 'result' not in order_response:
        flash('Error updating the cart.', 'error')
        return redirect(url_for('frontend.home'))

    order_items = order_response.get('result', {}).get('items', [])
    for item in order_items:
        product = ProductClient.get_product_by_id(item['product'])
        item['price'] = product['result']['price']
        item['name'] = product['result']['name']

    total_amount = sum(item['price'] * item['quantity'] for item in order_items)

    return render_template('order/cart.html', order_items=order_items , total_amount=total_amount)

from flask import request

@frontend_blueprint.route('/add_product', methods=['GET', 'POST'])
def add_product():
    form = forms.ProductForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        product_data = {
            'name': form.name.data,
            'price': form.price.data
        }
        try:
            response = ProductClient.add_product(product_data)
            if response:
                flash('Product added successfully', 'success')
                return redirect(url_for('frontend.home_vendor'))
            else:
                flash('Failed to add product', 'error')
        except requests.exceptions.ConnectionError:
            flash('Failed to connect to the server', 'error')
    return render_template('add_product.html', form=form)
