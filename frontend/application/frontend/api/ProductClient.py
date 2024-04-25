# application/frontend/api/ProductClient.py
import requests


class ProductClient:

    @staticmethod
    def get_products(vendor_id=None, min_price=None, max_price=None):
        params = {}
        
        if vendor_id is not None:
            params['vendor_id'] = vendor_id
            
        if min_price is not None:
            params['min_price'] = min_price
            
        if max_price is not None:
            params['max_price'] = max_price

        r = requests.get('http://cproduct-service:5002/api/products', params=params)
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
    def create_product(form, vendor_id):
        payload = {
            'name': form.name.data,
            'slug': form.slug.data,
            'image': "product1.jpg",
            'price': form.price.data,
            'vendor_id': vendor_id
        }
        response = requests.request("POST", url='http://cproduct-service:5002/api/product/create', data=payload)
        # product = response.json()
        return response
    
    
