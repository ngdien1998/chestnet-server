from flask import Flask

app = Flask(__name__)

from chestnet_classify.classifier.views import classifier
app.register_blueprint(classifier)