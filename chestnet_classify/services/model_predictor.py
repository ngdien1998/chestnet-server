from os import times
from numpy.lib.npyio import save
from scipy.ndimage.measurements import label
from tensorflow.keras.applications.densenet import DenseNet121
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2
from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.layers import Input, Dense
from tensorflow.keras.models import Model
from PIL import Image
import numpy as np
import cv2
import time
import os
from skimage.transform import resize

from chestnet_classify.services.gradcam import GradCAM
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

        predictions_dennsenet121 = Dense(15, activation='sigmoid', name='predictions')(base_model_dennsenet121.output)
        model_dennsenet121 = Model(inputs=img_input_dennsenet121, outputs=predictions_dennsenet121)
        model_dennsenet121.load_weights(settings['models']['densenet121']['weights'])

        # Mobilenet
        img_input_mobilenet = Input(shape=input_shape)
        base_model_mobilenet = MobileNetV2(include_top=False, input_tensor=img_input_mobilenet, input_shape=input_shape, pooling='avg', weights=None)
        predictions_mobilenet = Dense(15, activation='sigmoid', name='predictions')(base_model_mobilenet.output)

        model_mobilenet = Model(inputs=img_input_mobilenet, outputs=predictions_mobilenet)
        model_mobilenet.load_weights(settings['models']['mobilenet']['weights'])

        # VGG16
        img_input_vgg16 = Input(shape=input_shape)
        base_model_vgg16 = VGG16(include_top=False, input_tensor=img_input_vgg16, input_shape=input_shape, pooling="avg", weights=None)
        predictions_vgg16 = Dense(15, activation="sigmoid", name="predictions")(base_model_vgg16.output)
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

    @staticmethod
    def predict_labels(labels, predictions, thresholds):
        predicted_labels = []
        predicted_index = []
        for i, label in enumerate(labels):
            if predictions[i] > thresholds[i]:
                predicted_labels.append(label)
                predicted_index.append(i)
        
        if not predicted_labels:
            predicted_labels.append('No Finding')
            predicted_index.append(-1)

        return predicted_labels, predicted_index

    @staticmethod
    def calculate_heatmap(model, indices, labels, img_path):
        if indices[0] == -1:
            return img_path

        heatmap_images = []
        for i, label_index in enumerate(indices):
            orig_img = cv2.imread(img_path)
            image = ModelPredictor.preprocess_image(img_path)
            
            cam = GradCAM(model, label_index)
            heatmap = cam.compute_heatmap(image)
            heatmap = cv2.resize(heatmap, (orig_img.shape[1], orig_img.shape[0]))
            heatmap, output = cam.overlay_heatmap(heatmap, orig_img, alpha=0.5)

            image_path = f'images\\{time.time()}_{labels[i]}.png'
            save_path = os.path.join(settings['return_image_path'], image_path)
            print(save_path)
            cv2.imwrite(save_path, output)

            heatmap_images.append(image_path)

        return heatmap_images

    def make_predict(self, image_path, target_size=(224, 224)):
        processed_image = ModelPredictor.preprocess_image(image_path, target_size)
        
        densenet121_model = self.models[settings['models']['densenet121']['name']]
        mobilenet_model = self.models[settings['models']['mobilenet']['name']]
        vgg16_model = self.models[settings['models']['vgg16']['name']]

        predictions_densenet121 = densenet121_model.predict(processed_image)[0]
        predictions_mobilenet = mobilenet_model.predict(processed_image)[0]
        predictions_vgg16 = vgg16_model.predict(processed_image)[0]
        
        # w_a, w_b, w_c = settings['models']['densenet121']['auroc'], settings['models']['mobilenet']['auroc'], settings['models']['vgg16']['auroc']
        # cp = lambda a, b, c: round((a * w_a + b * w_b + c * w_c) / (w_a + w_b + w_c) * 100, 2)
        # pred_computed = list(zip(predictions_densenet121, predictions_mobilenet, predictions_vgg16))
        # pred_computed = [cp(x[0], x[1], x[2]) for x in pred_computed]

        pred_label_densenet121, pred_index_densenet121 = ModelPredictor.predict_labels(settings['labels'], predictions_densenet121, settings['models']['densenet121']['thresholds'])
        pred_label_mobilenet, pred_index_mobilenet = ModelPredictor.predict_labels(settings['labels'], predictions_mobilenet, settings['models']['mobilenet']['thresholds'])
        pred_label_vgg16, pred_index_vgg16 = ModelPredictor.predict_labels(settings['labels'], predictions_vgg16, settings['models']['vgg16']['thresholds'])

        heatmap_densenet121 = ModelPredictor.calculate_heatmap(densenet121_model, pred_index_densenet121, pred_label_densenet121, image_path)
        heatmap_mobilenet = ModelPredictor.calculate_heatmap(mobilenet_model, pred_index_mobilenet, pred_label_mobilenet, image_path)
        #heatmap_vgg16 = ModelPredictor.calculate_heatmap(vgg16_model, pred_index_vgg16, pred_label_vgg16, image_path)

        r = lambda arr: [round(x * 100, 2) for x in arr]

        return {
            'predictions_densenet121': { settings['labels'][i] : round(prediction.item() * 100, 2) for i, prediction in enumerate(predictions_densenet121) },
            'predictions_mobilenet': { settings['labels'][i] : round(prediction.item() * 100, 2) for i, prediction in enumerate(predictions_mobilenet) },
            'predictions_vgg16': { settings['labels'][i] : round(prediction.item() * 100, 2) for i, prediction in enumerate(predictions_vgg16) },
            #'predictions_compute': { settings['labels'][i] : prediction for i, prediction in enumerate(pred_computed) },
            'thresholds': {
                'densenet121': r(settings['models']['densenet121']['thresholds']),
                'mobilenet': r(settings['models']['mobilenet']['thresholds']),
                'vgg16': r(settings['models']['vgg16']['thresholds'])
            },
            'predictions_labels': {
                'densenet121': pred_label_densenet121,
                'mobilenet': pred_label_mobilenet
                #'vgg16': pred_label_vgg16
            },
            'heatmaps': {
                'densenet121': heatmap_densenet121,
                'mobilenet': heatmap_mobilenet
                #'vgg16': heatmap_vgg16
            }
        }
