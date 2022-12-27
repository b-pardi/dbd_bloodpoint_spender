import tensorflow as tf
import keras as k
import numpy as np
from parse import load_data

training_data = load_data('data/training')
validation_data = load_data('data/validation')

# sequential layers feed one output into the input of the next layer
model = k.Sequential()
# convolutional layer
model.add(k.layers.Convolution2D(32,3,3, input_shape=(img_width, img_height,3)))
model.add(k.Activation('relu'))
model.add(k.MaxPooling2D(pool_size=(2,2)))

model.add(k.Convolution2D(32,3,3, input_shape=(img_width, img_height,3)))
model.add(k.Activation('relu'))
model.add(k.MaxPooling2D(pool_size=(2,2)))

model.add(k.Convolution2D(32,3,3, input_shape=(img_width, img_height,3)))
model.add(k.Activation('relu'))
model.add(k.MaxPooling2D(pool_size=(2,2)))

# drop out layer
model.add(np.Flatten())