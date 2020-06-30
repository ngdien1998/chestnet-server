from chestnet_classify import app
from chestnet_classify.services import ModelPredictor

app.run(debug=True)
print('Load model...')
ModelPredictor.single()