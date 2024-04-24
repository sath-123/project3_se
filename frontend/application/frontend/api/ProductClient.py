# application/frontend/api/ProductClient.py
import requests


class ProductClient:

    @staticmethod
    def get_products():
        r = requests.get('http://cproduct-service:5002/api/products')
        products = r.json()
        return products

    @staticmethod
    def get_product(slug):
        response = requests.request(method="GET", url='http://cproduct-service:5002/api/product/' + slug)
        product = response.json()
        return product
    
    @staticmethod
    def get_product_by_id(product_id):
        response = requests.request(method="GET", url='http://cproduct-service:5002/api/product/' + str(product_id))
        product = response.json()
        return product
    
    @staticmethod
    def create_product(form):
        payload = {
            'name': form.name.data,
            'slug': form.slug.data,
            'image': form.image.data,
            'price': form.price.data,
            'vendor_id': form.vendor_id.data
        }
        response = requests.request("POST", url='http://cproduct-service:5002/api/product/create', data=payload)
        product = response.json()
        return product
    
    
