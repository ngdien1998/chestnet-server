import os
import base64
import time
from io import BytesIO
from PIL import Image
from chestnet_classify.app_settings import settings

def save_image(encoded_image):
    start_index = encoded_image.find(',') + 1
    image_data = encoded_image[start_index:]
    image_data = bytes(image_data, encoding='ascii')

    decode_image = base64.b64decode(image_data)
    image = Image.open(BytesIO(decode_image))

    image_path = os.path.join(settings['image_source_path'], f'{time.time()}.png')
    image.save(image_path)

    return image_path