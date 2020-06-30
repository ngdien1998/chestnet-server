settings = {
    'image_source_path': 'C:\\Users\\ngled\\OneDrive\\Desktop\\images',
    'models': {
        'densenet121': {
            'name': 'DenseNet121',
            'weights': 'C:\\Users\\ngled\\OneDrive\\Desktop\\chestnet-server\\weights-densenet121.h5'
        },
        'mobilenet': {
            'name': 'MobileNet',
            'weights': 'C:\\Users\\ngled\\OneDrive\\Desktop\\chestnet-server\\weights-mobilenet.h5'
        },
        'vgg16': {
            'name': 'VGG16',
            'weights': 'C:\\Users\\ngled\\OneDrive\\Desktop\\chestnet-server\\weights-vgg16.h5'
        }
    },
    'labels': ['Atelectasis', 'Cardiomegaly', 'Consolidation', 'Edema', 'Effusion', 'Emphysema', 'Fibrosis', 'Hernia', 'Infiltration', 'Mass', 'Nodule', 'Pleural_Thickening', 'Pneumonia', 'Pneumothorax']
}