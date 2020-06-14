import json
from flask import request, jsonify, Blueprint, abort
from flask.views import MethodView
from chestnet_classify import app

classifier = Blueprint('classifier', __name__)

@classifier.route('/')
def index():
    return 'Welcome chest XRAY multi-labels classifier'

class ClassifierView(MethodView):
    def get(self):
        return jsonify(['Hello world'])

classifier_view = ClassifierView.as_view('classifier_view')
app.add_url_rule('/classify', view_func=classifier_view, methods=['GET'])
