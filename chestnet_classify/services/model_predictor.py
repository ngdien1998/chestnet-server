from tensorflow.keras.applications.densenet import DenseNet121
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2
from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.layers import Input, Dense
from tensorflow.keras.models import Model
from PIL import Image
import numpy as np
from skimage.transform import resize

from chestnet_classify.app_settings import settings

class ModelPredictor:
    __instance = None

    def __init__(self):
        if ModelPredictor.__instance == None:
            self.models = self.__get_models()
            print('Model loaded')
        else:
            raise Exception('Singleton class cannot be initialized')

    def __get_models(self):
        input_shape=(224, 224, 3)

        # Densenet121
        img_input_dennsenet121 = Input(shape=input_shape)
        base_model_dennsenet121 = DenseNet121(include_top=False, input_tensor=img_input_dennsenet121, input_shape=input_shape, pooling='avg', weights=None)

        predictions_dennsenet121 = Dense(14, activation='sigmoid', name='predictions')(base_model_dennsenet121.output)
        model_dennsenet121 = Model(inputs=img_input_dennsenet121, outputs=predictions_dennsenet121)
        model_dennsenet121.load_weights(settings['models']['densenet121']['weights'])

        # Mobilenet
        img_input_mobilenet = Input(shape=input_shape)
        base_model_mobilenet = MobileNetV2(include_top=False, input_tensor=img_input_mobilenet, input_shape=input_shape, pooling='avg', weights=None)
        predictions_mobilenet = Dense(14, activation='sigmoid', name='predictions')(base_model_mobilenet.output)

        model_mobilenet = Model(inputs=img_input_mobilenet, outputs=predictions_mobilenet)
        model_mobilenet.load_weights(settings['models']['mobilenet']['weights'])

        # VGG16
        img_input_vgg16 = Input(shape=input_shape)
        base_model_vgg16 = VGG16(include_top=False, input_tensor=img_input_vgg16, input_shape=input_shape, pooling="avg", weights=None)
        predictions_vgg16 = Dense(14, activation="sigmoid", name="predictions")(base_model_vgg16.output)
        model_vgg16 = Model(inputs=img_input_vgg16, outputs=predictions_vgg16)
        model_vgg16.load_weights(settings['models']['vgg16']['weights'])

        return {
            settings['models']['densenet121']['name']: model_dennsenet121,
            settings['models']['mobilenet']['name']: model_mobilenet,
            settings['models']['vgg16']['name']: model_vgg16,
        }

    @staticmethod
    def single():
        if ModelPredictor.__instance == None:
            print('Initializing predictor...')
            ModelPredictor.__instance = ModelPredictor()
        
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
        
        predictions_densenet121 = self.models[settings['models']['densenet121']['name']].predict(processed_image)[0]
        predictions_mobilenet = self.models[settings['models']['mobilenet']['name']].predict(processed_image)[0]
        predictions_vgg16 = self.models[settings['models']['vgg16']['name']].predict(processed_image)[0]

        return {
            'predictions_densenet121': { settings['labels'][i] : prediction.item() for i, prediction in enumerate(predictions_densenet121) },
            'predictions_mobilenet': { settings['labels'][i] : prediction.item() for i, prediction in enumerate(predictions_mobilenet) },
            'predictions_vgg16': { settings['labels'][i] : prediction.item() for i, prediction in enumerate(predictions_vgg16) }
        }
