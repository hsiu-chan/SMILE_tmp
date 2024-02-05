from tensorflow.keras import layers, models, utils,callbacks
# one-hot encoding
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import *
from tensorflow.keras.utils import plot_model
import tensorflow as tf


def vgg16_model(input_shape,num_class):
    model = Sequential([
        Conv2D(64, (3,3), padding='same', activation='relu', input_shape=input_shape),
        Conv2D(64, (3,3), padding='same', activation='relu'),
        MaxPooling2D(pool_size=(2,2)),
        Conv2D(128, (3,2), padding='same', activation='relu'),
        Conv2D(128, (3,3), padding='same', activation='relu'),
        MaxPooling2D(pool_size=(2,2)),
        Conv2D(256, (3,3), padding='same', activation='relu'),
        Conv2D(256, (3,3), padding='same', activation='relu'),
        Conv2D(256, (3,3), padding='same', activation='relu'),
        MaxPooling2D(pool_size=(2,2)),
        Conv2D(512, (3,3), padding='same', activation='relu'),
        Conv2D(512, (3,3), padding='same', activation='relu'),
        Conv2D(512, (3,3), padding='same', activation='relu'),
        MaxPooling2D(pool_size=(2,2)),
        Conv2D(512, (3,3), padding='same', activation='relu'),
        Conv2D(512, (3,3), padding='same', activation='relu'),
        Conv2D(512, (3,3), padding='same', activation='relu'),
        MaxPooling2D(pool_size=(2,2)),
        #Flatten(),
        
        
        GlobalAveragePooling2D(),
        Dense(1000,activation='relu'),
        Dropout(0.3),
        Dense(1000,activation='relu'),
        Dropout(0.3),
        Dense(num_class,activation='softmax'),
    ])
    return model


def GoogLeNet_model(input_shape,num_class):
    def inception(x, nb_filter):
        branch1x1 = Conv2D(nb_filter, (1,1), padding='same', activation='relu')(x)
    
        branch3x3 = Conv2D(nb_filter, (1,1), padding='same', activation='relu')(x)
        branch3x3 = Conv2D(nb_filter, (3,3), padding='same', activation='relu')(branch3x3)
    
        branch5x5 = Conv2D(nb_filter, (1,1), padding='same', activation='relu')(x)
        branch5x5 = Conv2D(nb_filter, (5,5), padding='same', activation='relu')(branch5x5)
    
        branchpool = MaxPooling2D(pool_size=(3,3), strides=(1,1), padding='same')(x)
        branchpool = Conv2D(nb_filter, (1,1), padding='same', activation='relu')(branchpool)
    
        x = concatenate([branch1x1, branch3x3, branch5x5, branchpool], axis=-1)
    
        return x
 
    inputs = Input(shape=input_shape)
    x = Conv2D(64, (7,7), padding='same', strides=(2,2), activation='relu')(inputs)
    x = MaxPooling2D(pool_size=(3,3), strides=(2,2), padding='same')(x)
    x = Conv2D(192, (3,3), padding='same', activation='relu')(x)
    x = MaxPooling2D(pool_size=(3,3), strides=(2,2), padding='same')(x)
    x = inception(x,64)
    x = inception(x,120)
    x = MaxPooling2D(pool_size=(3,3), strides=(2,2), padding='same')(x)
    x = inception(x,128)
    x = inception(x,128)
    x = inception(x,128)
    x = inception(x,132)
    x = inception(x,208)
    x = MaxPooling2D(pool_size=(3,3), strides=(2,2), padding='same')(x)
    x = inception(x,208)
    x = inception(x,256)
    
    x = GlobalAveragePooling2D()(x)
    x = Dropout(0.4)(x)
    x = Dense(1000, activation='relu')(x)
    x = Dense(num_class, activation='softmax')(x)
    model = Model(inputs, x)
    return model
