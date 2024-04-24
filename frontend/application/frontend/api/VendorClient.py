# application/frontend/api/UserClient.py
import requests
from flask import session, request
import sys

class VendorClient:
    @staticmethod
    def post_login(form):
        api_key = False
        payload = {
            'username': form.username.data,
            'password': form.password.data
        }
        url = 'http://cvendor-service:5004/api/vendor/login'
        response = requests.request("POST", url=url, data=payload)
        if response:
            d = response.json()
            print("This is response from vendor api: " + str(d))
            if d['api_key'] is not None:
                api_key = d['api_key']
        return api_key

    @staticmethod
    def get_user():

        headers = {
            'Authorization': 'Basic ' + session['user_api_key']
        }
        url = 'http://cvendor-service:5004/api/vendor'
        response = requests.request(method="GET", url=url, headers=headers)
        user = response.json()
        return user

    @staticmethod
    def post_vendor_create(form):
        print("Vendor Client: post_vendor_create", file=sys.stderr)
        user = False
        payload = {
            'email': form.email.data,
            'password': form.password.data,
            'first_name': form.first_name.data,
            'last_name': form.last_name.data,
            'username': form.username.data
        }
        url = 'http://cvendor-service:5004/api/vendor/create'
        response = requests.request("POST", url=url, data=payload)
        if response:
            user = response.json()
        return user

    @staticmethod
    def does_exist(username):
        # url = 'http://cvendor-service:5004/api/vendor/' + username + '/exists'
        # response = requests.request("GET", url=url)
        return False

