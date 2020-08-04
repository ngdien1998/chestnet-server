settings = {
    'image_source_path': 'C:\\Users\\ngled\\OneDrive\\Desktop\\images',
    'return_image_path': 'C:\\Users\\ngled\\OneDrive\\Desktop\\chestnet-server\\chestnet_classify\\client',
    'data_desc_path': 'C:\\Users\\ngled\\OneDrive\\Desktop\\chestnet-server\\chestnet_classify\\data\\Data_Entry_2017.csv',
    'models': {
        'densenet121': {
            'name': 'DenseNet121',
            'weights': 'C:\\Users\\ngled\\OneDrive\\Desktop\\chestnet-server\\weights-densenet121.h5',
            'thresholds': [0.09312474727630615, 0.00814768671989441, 0.037762463092803955, 8.368492126464844e-05, 0.01647046208381653, 0.10989829897880554, 0.01093253493309021, 0.008378952741622925, 0.000746309757232666, 0.23427608609199524, 0.033830076456069946, 0.062426745891571045, 0.021347999572753906, 0.011091738939285278, 0.025962144136428833],
            'auroc': 0.79
        },
        'mobilenet': {
            'name': 'MobileNet',
            'weights': 'C:\\Users\\ngled\\OneDrive\\Desktop\\chestnet-server\\weights-mobilenet.h5',
            'thresholds': [0.08642596006393433, 0.006453573703765869, 0.055340707302093506, 0.05066439509391785, 0.027385979890823364, 0.12745416164398193, 0.033603280782699585, 0.009231358766555786, 0.0012461841106414795, 0.258659303188324, 0.0461086630821228, 0.06760656833648682, 0.03664755821228027, 0.012873649597167969, 0.03218600153923035],
            'auroc': 0.78
        },
        'vgg16': {
            'name': 'VGG16',
            'weights': 'C:\\Users\\ngled\\OneDrive\\Desktop\\chestnet-server\\weights-vgg16.h5',
            'thresholds': [0.1139782965183258, 0.022444099187850952, 0.055227071046829224, 0.004459351301193237, 0.02779403328895569, 0.15331220626831055, 0.01959928870201111, 0.01194337010383606, 0.001346588134765625, 0.21599239110946655, 0.049256831407547, 0.052085310220718384, 0.032029569149017334, 0.009415894746780396, 0.048362553119659424],
            'auroc': 0.61
        }
    },
    'labels': ['Atelectasis', 'Cardiomegaly', 'Consolidation', 'Covid19', 'Edema', 'Effusion', 'Emphysema', 'Fibrosis', 'Hernia', 'Infiltration', 'Mass', 'Nodule', 'Pleural_Thickening', 'Pneumonia', 'Pneumothorax']
}