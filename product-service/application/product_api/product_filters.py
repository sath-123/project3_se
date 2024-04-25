from ..models import Product
from flask import jsonify, request
import sys

class ProductFilterFactory:
    @staticmethod
    def create_filter(strategy, vendor_id=None, min_price=None, max_price=None):
        if strategy == 'vendor':
            return VendorFilter(vendor_id)
        elif strategy == 'price_range':
            return PriceRangeFilter(min_price, max_price)
        elif strategy == 'vendor_price_range':
            return VendorPriceRangeFilter(vendor_id, min_price, max_price)
        else:
            return NoFilter()


class VendorFilter:
    def __init__(self, vendor_id):
        self.vendor_id = vendor_id

    def apply(self, query):
        if self.vendor_id:
            return query.filter_by(vendor_id=self.vendor_id)
        return query

class PriceRangeFilter:
    def __init__(self, min_price, max_price):
        self.min_price = min_price
        self.max_price = max_price

    def apply(self, query):
        if self.min_price:
            query = query.filter(Product.price >= self.min_price)
        if self.max_price:
            query = query.filter(Product.price <= self.max_price)
        return query

class VendorPriceRangeFilter:
    def __init__(self, vendor_id, min_price, max_price):
        self.vendor_id = vendor_id
        self.min_price = min_price
        self.max_price = max_price

    def apply(self, query):
        if self.vendor_id:
            query = query.filter_by(vendor_id=self.vendor_id)
        if self.min_price:
            query = query.filter(Product.price >= self.min_price)
        if self.max_price:
            query = query.filter(Product.price <= self.max_price)
        return query

class NoFilter:
    def apply(self, query):
        return query
