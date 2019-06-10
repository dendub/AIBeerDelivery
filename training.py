from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense
from keras.models import model_from_json
from keras.preprocessing import image
import numpy as np
from keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import random,os


classifier = Sequential()

classifier.add(Conv2D(32, (3, 3), input_shape = (64, 64, 3), activation = 'relu')) #convolutional layer with number of filters its shape, resolution of picture and 3 (RGB)

classifier.add(MaxPooling2D(pool_size = (2, 2))) #polling operation with 2x2 matrix

classifier.add(Flatten())

classifier.add(Dense(units = 128, activation = 'relu')) #hidden layers with number of nodes

classifier.add(Dense(units = 1, activation = 'sigmoid')) #output node which will give binary output

classifier.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy']) #stochastic gradient algorithm, loss parametr metrics parameter


#IMAGE PREAPRATIONS
train_datagen = ImageDataGenerator(rescale = 1./255,
                                   shear_range = 0.2,
                                   zoom_range = 0.2,
                                   horizontal_flip = True)
test_datagen = ImageDataGenerator(rescale = 1./255)
training_set = train_datagen.flow_from_directory('training_set',
target_size = (64, 64),
batch_size = 32,
class_mode = 'binary')
test_set = test_datagen.flow_from_directory('test_set',
target_size = (64, 64),
batch_size = 32,
class_mode = 'binary')

#FITTING DATA INTO MODEL
classifier.fit_generator(training_set,
steps_per_epoch = 379,
epochs = 3,
validation_data = test_set,
validation_steps = 216)


model_jason =classifier.to_json()
with open("model.json", "w") as json_file:
    json_file.write(model_jason)
classifier.save_weights("model.h5")
print("Saved")