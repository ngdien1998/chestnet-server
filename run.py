from chestnet_classify import app
from chestnet_classify.services import ModelPredictor

print('Load model...')
ModelPredictor.single()

if __name__ == "__main__":
    app.run(debug=True)