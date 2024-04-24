# application/product_api/routes.py
from . import product_api_blueprint
from .. import db
from ..models import Product
from flask import jsonify, request
import sys


@product_api_blueprint.route('/api/products', methods=['GET'])
def products():
    items = []
    for row in Product.query.all():
        items.append(row.to_json())

    response = jsonify({'results': items})
    return response


@product_api_blueprint.route('/api/product/create', methods=['POST'])
def post_create():

    print(request.form, file=sys.stderr)

    id = request.form['id']
    name = request.form['name']
    slug = request.form['slug']
    image = request.form['image']
    price = request.form['price']
    vendor_id = request.form['vendor_id']

    item = Product()
    item.name = name
    item.slug = slug
    item.image = image
    item.price = price
    item.vendor_id = vendor_id
    item.id = id


    db.session.add(item)
    db.session.commit()

    response = jsonify({'message': 'Product added', 'product': item.to_json()})
    return response


@product_api_blueprint.route('/api/product/<string:slug>', methods=['GET'])
def product(slug):
    print("In the call slug" , file=sys.stderr)
    item = Product.query.filter_by(slug=slug).first()
    if item is not None:
        response = jsonify({'result': item.to_json()})
    else:
        response = jsonify({'message': 'Cannot find product'}), 404
    return response


@product_api_blueprint.route('/api/product/<int:product_id>', methods=['GET'])
def get_product_by_id(product_id):

    print("In the call" , file=sys.stderr)
    print("product_id", product_id, file=sys.stderr )
    item = Product.query.filter_by(id=product_id).first()
    if item is not None:
        response = jsonify({'result': item.to_json()})
    else:
        response = jsonify({'message': 'Cannot find product by id'}), 404

    print(response, file=sys.stderr)
    return response


