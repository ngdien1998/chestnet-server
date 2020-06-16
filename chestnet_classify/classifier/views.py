import json
from flask import request, jsonify, Blueprint, abort
from flask.views import MethodView

from chestnet_classify import app
from chestnet_classify.services.process_image import save_image
from chestnet_classify.services import ModelPredictor
from chestnet_classify.app_settings import settings

classifier = Blueprint('classifier', __name__)

@classifier.route('/')
def index():
    return 'Welcome chest XRAY multi-labels classifier'

class ClassifierView(MethodView):
    def post(self):
        message = request.get_json(force=True)
        encoded_image = message['image']

        image_path = save_image(encoded_image)

        densenet121 = settings['models']['densenet121']['name']
        weights = settings['models']['densenet121']['weights']
        print(densenet121, weights)

        result = ModelPredictor.get(model_name=densenet121, model_weight=weights).make_predict(image_path)
        return jsonify({
            'data': {
                'success': True,
                'result': result
            }
        })

classifier_view = ClassifierView.as_view('classifier_view')
app.add_url_rule('/classify', view_func=classifier_view, methods=['POST'])
