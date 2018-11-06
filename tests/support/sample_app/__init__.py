""" Sample Protean Flask app for testing"""
from flask import Flask

from protean_flask import Protean
from .views import ShowDogResource, CreateDogResource, UpdateDogResource, \
    DeleteDogResource, ListDogResource, flask_view

app = Flask(__name__)
api = Protean(app)

app.add_url_rule('/dogs/<int:identifier>',
                 view_func=ShowDogResource.as_view('show_dog'),
                 methods=['GET'])
app.add_url_rule('/dogs',
                 view_func=CreateDogResource.as_view('create_dog'),
                 methods=['POST'])
app.add_url_rule('/dogs',
                 view_func=ListDogResource.as_view('list_dogs'),
                 methods=['GET'])
app.add_url_rule('/dogs/<int:identifier>',
                 view_func=UpdateDogResource.as_view('update_dog'),
                 methods=['PUT'])
app.add_url_rule('/dogs/<int:identifier>',
                 view_func=DeleteDogResource.as_view('delete_dog'),
                 methods=['DELETE'])
app.add_url_rule('/flask-view', view_func=flask_view,
                 methods=['GET'])
