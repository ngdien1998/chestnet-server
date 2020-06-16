from tensorflow.keras.applications.densenet import DenseNet121
from tensorflow.keras.layers import Input, Dense
from tensorflow.keras.models import Model
from PIL import Image
import numpy as np
from skimage.transform import resize

from chestnet_classify.app_settings import settings

class ModelPredictor:
    __instance = None

    def __init__(self, model_name, model_weight, input_shape=(224, 224, 3)):
        if ModelPredictor.__instance == None:
            self.model = self.__get_model(model_name, model_weight, input_shape)
            if not self.model:
                raise ValueError('Invalid model. Only support DenseNet121, MobileNet, VGG16, VGG19.')

            ModelPredictor.__instance = self
        else:
            raise Exception('Singleton class cannot be initialized')

    def __get_model(self, model_name, model_weight, input_shape=(224, 224, 3)):
        img_input = Input(shape=input_shape)
        if model_name == settings['models']['densenet121']['name']:
            base_model = DenseNet121(include_top=False, input_tensor=img_input, input_shape=input_shape, pooling='avg', weights=None)

            predictions = Dense(14, activation='sigmoid', name='predictions')(base_model.output)
            model = Model(inputs=img_input, outputs=predictions)
            model.load_weights(model_weight)

        return model

    @staticmethod
    def get(model_name, model_weight):
        if ModelPredictor.__instance == None:
            print('Initializing predictor...')
            ModelPredictor(model_name, model_weight)
        
        return ModelPredictor.__instance

    @staticmethod
    def preprocess_image(image_path, target_size=(224, 224)):
        img = Image.open(image_path)
        img = img.convert('RGB')
        img = np.asarray(img) / 255.
        img = resize(img, target_size)
        img = np.expand_dims(img, axis=0)
        
        return img

    def make_predict(self, image_path, target_size=(224, 224)):
        processed_image = ModelPredictor.preprocess_image(image_path, target_size)
        predictions = self.model.predict(processed_image)[0]
        return { settings['labels'][i] : prediction.item() for i, prediction in enumerate(predictions) }
