from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense
from keras.preprocessing import image
import numpy as np
from keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from random import *
import os
from keras.models import model_from_json

#classifier = Sequential()

#classifier.add(Conv2D(32, (3, 3), input_shape = (64, 64, 3), activation = 'relu'))

#classifier.add(MaxPooling2D(pool_size = (2, 2)))

#classifier.add(Flatten())

#classifier.add(Dense(units = 128, activation = 'relu'))

#classifier.add(Dense(units = 1, activation = 'sigmoid'))

#classifier.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])

#train_datagen = ImageDataGenerator(rescale = 1./255,
#                                   shear_range = 0.2,
#                                   zoom_range = 0.2,
#                                   horizontal_flip = True)
#test_datagen = ImageDataGenerator(rescale = 1./255)
#training_set = train_datagen.flow_from_directory('training_set',
#target_size = (64, 64),
#batch_size = 32,
#class_mode = 'binary')
#test_set = test_datagen.flow_from_directory('test_set',
#target_size = (64, 64),
#batch_size = 32,
#class_mode = 'binary')


#classifier.fit_generator(training_set,
#steps_per_epoch = 379,
#epochs = 1,
#validation_data = test_set,
#validation_steps = 216)

#path = "dataset\single_prediction"
#random_filename = random.choice([
#    x for x in os.listdir(path)
#    if os.path.isfile(os.path.join(path, x))
#])
#img1=mpimg.imread(random_filename)
#imgplot = plt.imshow(img1)
#plt.show()
from pip._vendor.distlib.compat import raw_input

json_file = open('model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
loaded_model.load_weights("model.h5")


#for r, d, f in os.walk('dataset/single_prediction/'):
#    file = choice(f)

FILE_NAME = raw_input('Enter a filename: ')


test_image = image.load_img(FILE_NAME, target_size = (64, 64))
test_image = image.img_to_array(test_image)
test_image = np.expand_dims(test_image, axis = 0)
result = loaded_model.predict(test_image)
#print(result)
#training_set.class_indices
if result[0][0] == 1:
    prediction = 'glass'
else:
    prediction = 'can'

img=mpimg.imread(FILE_NAME)
imgplot = plt.imshow(img)
plt.show()

print(prediction)
