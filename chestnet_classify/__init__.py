from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

from chestnet_classify.classifier.views import classifier
app.register_blueprint(classifier)