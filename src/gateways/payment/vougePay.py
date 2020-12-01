#::::::::::::::::::::::::::::::::::::::::::::
# a python script to access vougepay API   ::
# for creating user accounts for shoppers  ::
# for processing checkout invoices         ::
# handling payments                        ::
# keeping records (on vougepay)            ::
# moving funds directly to (on vougepay)   ::
# merchants banks (on vendora)             ::
#::----------------------------------------::
#   Auhtor : Joel Tanko                    ::
#::::::::::::::::::::::::::::::::::::::::::::


import json
import hashlib
from datetime import datetime
from random import randint
import requests
from store.models import Store


# Globals
api = 'https://voguepay.com/api/'    # vougepay API Endpoint
API_token = 'pwEZ9aEA2ZTRgYZttYzTbCmerxk7em'   # vendora APIToken
email = 'urich2ogofe@gmail.com'    # vendora Vougepay email
merchant_id = '4951-0111766'     # vendora merchant_id


def jsonify(content):
    "convert data to json"
    command = json.JSONEncoder().encode(content)
    return command


def expected_hash(response, salt, expected):
    "compares hashes to verify transaction"




class Create:
    """ 
    Creates a new Vouge merchant instance after a new store is opened. 
    Where: 
    ::::::::::::::::::::::::params::::::::::::::::::::::::::::::::::::::
    :::     username    : user.usernme                               :::
    :::     password    : user.password()                            :::
    :::     currency    : store.currency.code                        :::
    :::     country     : store.country                              :::
    :::     first_name  : user.first_name                            :::
    :::     last_name   : user.last_name                             :::
    :::     email       : user.email                                 :::
    ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    """
    def __init__(self, first_name:str, last_name:str, username:str, password:str, email:str, country:str, currency:str):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = password
        self.email = email
        self.country = country
        self.currency = currency
        self.task = 'create'
        self.create()

    def __str__(self):
        return self.name()

    def name(self):
        " return full name"
        return f'{self.first_name} {self.last_name}'
    
    def create(self):
        "command vouge api to create new user"
        ref = self.genRef()
        pre_hash = API_token + self.task + email + ref
        hash_ = hashlib.sha512(pre_hash.encode()).hexdigest()
        command = {
            'task': 'create',   # create an account
            'merchant': merchant_id, # my merchant ID
            'ref' : ref,
            'hash' : hash_,
            'list' : self._list()
        }
        response = requests.post(url=api, data=command, json=jsonify(command)).json()  # send a post request to the API
        if response == 'OK':
            return (True, "OK", "Successful")
        elif not expected_hash(response, response['salt'], hash_):
            return (False, "BAD", "Fatal")
        else:
            return (False, "BAD", "Fatal")

    def _list(self):
        list_ = {
            'username': self.username,
            'password': self.password,
            'email': self.email,
            'firstname': self.first_name,
            'lastname': self.last_name,
            'referrer': email,
            'country': self.country,
            'currency': self.currency,
        }
        return (list_)

    def genRef(self):
        " creates a unique reference ID"
        ref = ''
        now = datetime.now()
        for i in range(10):
            ref += str(randint(0, 9))
        unique_id = str(now.date()) + ref + str(randint(0, 26123926646443674)) + str(now.timestamp())
        return (unique_id)


class Order:
    " Handles order proceesing on checkout views. "
    def __init__(self, invoice:dict, merchant_id:int, store:Store, user:dict):
        self.invoice = store
        self.merchant = merchant_id
        self.buyer = user
        self.seller = store
        self.task = 'pay'

    def genRef(self):
        " creates a unique reference ID"
        now = datetime.now()
        ref = ''
        for i in range(10):
            ref += str(randint(0, 9))
        unique_id = str(now.date()) + ref + str(randint(0, 26123926646443674)) + str(now.timestamp())
        return (unique_id)

    def getToken(self):
        "get the api token of the store owner from vouge"
        token = requests.get(
            url=api
        )
        return token

    def pay(self, card:dict, amt:float):
        " Payment handler with vouge for store checkout. "
        ref = self.genRef()
        token = self.getToken()
        pre_hash = str(token) + self.task + self.seller.owner.email + ref
        hash_ = hashlib.sha512(pre_hash.encode()).hexdigest()
        details = {
            'task': 'pay',
            'merchant_id': self.merchant,
            'ref' : ref,
            'hash': hash_,
            'amount': amt,
            'seller':self.seller.owner.email,
            'memo': "Checkout from %s." % self.seller.name
        }
        response = requests.post(
            url=api,
            data=details,
            json=jsonify(details)
        ).json()
        if response == 'OK':
            self.withdraw(amt)
            return (True, "OK", "Successful")
        elif not expected_hash(response, response['salt'], hash_):
            return (False, "BAD", "Fatal")
        else:
            return (False, "BAD", "Fatal")
    
    def withdraw(self, amt:float):
        "Automatically send payment into merchant account"
        ref = self.genRef()
        token = self.getToken()
        pre_hash = str(token) + self.task + self.seller.owner.email + ref
        hash_ = hashlib.sha512(pre_hash.encode()).hexdigest()
        details = {
            'task': 'withdraw',
            'merchant': self.merchant,
            'ref' : ref,
            'hash': hash_,
            'amount': amt,
            'bank_name' : self.seller.owner.bank_name,
            'bank_acct_name' : self.seller.owner.bank_acct_name,
            'bank_currency' : self.seller.currency,
            'bank_country' : self.seller.owner.country
        }
        response = requests.post(
            url=api,
            data=details,
            json=jsonify(details)
        ).json()
        if response == 'OK':
            return (True, "OK", "Successful")
        elif not expected_hash(response, response['salt'], hash_):
            return (False, "BAD", "Fatal")
        else:
            return (False, "BAD", "Fatal")