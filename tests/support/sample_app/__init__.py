""" Sample Protean Flask app for testing"""
from flask import Flask

from protean_flask import Protean
from .views import ShowDogResource

app = Flask(__name__)
api = Protean(app)

app.add_url_rule('/dogs/<int:identifier>',
                 view_func=ShowDogResource.as_view('show_dog'))
