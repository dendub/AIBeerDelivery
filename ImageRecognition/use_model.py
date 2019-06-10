from keras.models import model_from_json
import cv2
import numpy as np


json_file = open('model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)

loaded_model.load_weights("model.h5")


loaded_model.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])

FILE_NAME = "./data/1.coin.jpg"

img = cv2.imread(FILE_NAME)
img = cv2.resize(img, (50,50))
print(img.shape)
img = img.reshape(1, 50, 50, 3)

print(img.shape)

if (loaded_model.predict(img)[0] == 0):
    print('This is Bill')
else:
    print('This is Coin')
