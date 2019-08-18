
# from keras import models, layers
# from keras import Input
from keras.models import load_model
from keras.preprocessing.image import ImageDataGenerator
# from keras import optimizers, initializers, regularizers, metrics
# from keras.callbacks import ModelCheckpoint, EarlyStopping
# from keras.layers import BatchNormalization, Conv2D, Activation, Dense, GlobalAveragePooling2D, MaxPooling2D, ZeroPadding2D, Add
import json
import os
import matplotlib.pyplot as plt
import numpy as np
import math


def get_text_image():
    
    """
    잘려진 conotur가 텍스트인지 아닌지 판단합니다. 
    :param contour_path: gray-scale 처리된 contour가 저장된 경로 
    :return: output[0] = 0이면 negative(not_text),
             output[0] == 1이면 positive(text)
    """
    model = load_model('saved_models/softmax_model_v2.h5')
    val_datagen = ImageDataGenerator(rescale=1./255)
    
    val_dir = os.path.join('new/')
    val_generator = val_datagen.flow_from_directory(val_dir, batch_size=1, target_size=(78, 78), color_mode='grayscale')
    output = model.predict_generator(val_generator, steps=1)
    output[output>=0.5] = 1 
    output[output<0.5] = 0
    
    if(output[0][0]==1):
        #pass
        print('1: ', output)
        return 'text'
    else:
        #save 
        print('0: ', output)
        return 'not_text'

    print(output)
    print(val_generator.class_indices)


if __name__ == "__main__":
    get_text_image()