import os
from tqdm import tqdm
import cv2

TRAIN_DIR = './train'
IMG_SIZE = 50



def create_train_test_dir():
    counter=1
    for img in tqdm(os.listdir(TRAIN_DIR)):
    	word_label = img.split('.')[1]
    	if word_label == 'bill': lable="bill"
    	elif word_label == 'coin': lable="coin"
    	path = os.path.join(TRAIN_DIR,img)
    	img = cv2.imread(path,cv2.IMREAD_GRAYSCALE)
    	img = cv2.resize(img, (IMG_SIZE,IMG_SIZE))
    	cv2.imwrite("./training_data/"+lable+'/'+str(counter)+'.jpg',img)
    	counter += 1


create_train_test_dir()
