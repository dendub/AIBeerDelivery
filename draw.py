import random, time
import sys
import pygame
import numpy as np
import ptext
import beer_recommender
from textgenrnn import textgenrnn
from keras.models import model_from_json
import cv2
from random import choice
import os
from keras.models import model_from_json
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from keras.preprocessing import image
from pip._vendor.distlib.compat import raw_input

def canOrGalss():
    json_file = open('model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    loaded_model.load_weights("model.h5")

    # for r, d, f in os.walk('dataset/single_prediction/'):
    #    file = choice(f)

    FILE_NAME = raw_input('Enter a filename: ')

    test_image = image.load_img(FILE_NAME, target_size=(64, 64))
    test_image = image.img_to_array(test_image)
    test_image = np.expand_dims(test_image, axis=0)
    result = loaded_model.predict(test_image)
    # print(result)
    # training_set.class_indices
    if result[0][0] == 1:
        prediction = 'glass'
    else:
        prediction = 'can'

    img = mpimg.imread(FILE_NAME)
    imgplot = plt.imshow(img)
    plt.show()

    print(prediction)


def recMoney():

    print("CLIENT GIVES MONEY")
    time.sleep(2)

    json_file = open('ImageRecognition/model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)

    loaded_model.load_weights("ImageRecognition/model.h5")

    loaded_model.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])

    for r, d, f in os.walk('./ImageRecognition/data/'):
        file = choice(f)


    FILE_NAME = "./ImageRecognition/data/" + file

    pygame.init()
    money = pygame.image.load(FILE_NAME).convert()

    font = pygame.font.SysFont("comicsansms", 50)

    size = width, height = 300, 300
    screen = pygame.display.set_mode(size)

    screen.blit(pygame.transform.scale(money, (300, 300)), (0, 0))

    pygame.display.flip()

    time.sleep(3)




    img = cv2.imread(FILE_NAME)
    img = cv2.resize(img, (50,50))
    img = img.reshape(1, 50, 50, 3)


    if (loaded_model.predict(img)[0] == 0):
        print("CLIENT GAVE BILL")
    else:
        print("CLIENT GAVE COIN")



def newbeer():
    textgen = textgenrnn(weights_path='newbeer/colaboratory_weights.hdf5',
                           vocab_path='newbeer/colaboratory_vocab.json',
                           config_path='newbeer/colaboratory_config.json')

    # textgen.generate_samples(max_gen_length=20, temperature=0.8)
    textgen.generate_to_file('newbeer/textgenrnn_texts.txt', max_gen_length=3, temperature=3)

    f=open("newbeer/textgenrnn_texts.txt", "r")

    for l in f:
        texts = l
    texts = texts.replace('\n', '').split(' ')
    pygame.init()
    beer = pygame.image.load("newbeer/beer.png")
    beerrect = beer.get_rect()

    font = pygame.font.SysFont("comicsansms", 50)

    size = width, height = beerrect.width, beerrect.height
    screen = pygame.display.set_mode(size)

    beerrect.center = (width/2, height/2)
    screen.blit(beer, beerrect)

    y = height/2 + 50
    for t in texts:
        text = font.render(t, True, (20, 20, 20))
        screen.blit(text, (width/2 - text.get_width() // 2, y))
        y = y + text.get_height()

    pygame.display.flip()

    time.sleep(10)


def direction(prev, next):
    step = (prev[0] - next[0], prev[1] - next[1])
    if step == (1, 0):
        return 0
    if step == (-1, 0):
        return 2
    if step == (0, 1):
        return 1
    if step == (0, -1):
        return 3



def draw(map, steps):
    steps = steps[::-1]

    map = np.asarray(map)
    pygame.init()
    grid = pygame.image.load("media/grid.png")
    home = pygame.image.load("media/barricade.png")
    agent = pygame.image.load("media/agent2.png")
    warehouse = pygame.image.load("media/home.png")
    step = pygame.image.load("media/step.png")
    gridrect = agent.get_rect()
    homerect = home.get_rect()
    agentrect = agent.get_rect()
    warehouserect = warehouse.get_rect()
    steprect = step.get_rect()
    w, h = gridrect.width, gridrect.height

    size = width, height = len(map[0])*w, len(map)*h
    screen = pygame.display.set_mode(size)


    y = h/2
    for line in map:
        x = w/2
        for obj in line:
            if obj == 0:
                gridrect.center = (x, y)
                screen.blit(grid, gridrect)
            if obj == 1:
                homerect.center = (x, y)
                screen.blit(home, homerect)

            x += w
        y += h




    warehouserect.center = ((steps[-1][1])*w + w/2, (steps[-1][0])*h+h/2)
    screen.blit(warehouse, warehouserect)


    for s, ns in zip(steps[0: -1], steps[1:]):
        agentrect.center = ((s[1])*w + w/2, (s[0])*h+h/2)

        newdir = direction(s, ns)

        screen.blit(pygame.transform.rotate(agent, 90*newdir), agentrect)
        pygame.display.flip()

        time.sleep(0.01)

        steprect.center = ((s[1])*w + w/2, (s[0])*h+h/2)
        screen.blit(step, steprect)

    while(True):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                     sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    posX, posY = pygame.mouse.get_pos()
                    if(posX >= 0 and posX <= 20 and posY >=380 and posY <=400):
                        if (input("If you want to see smart beer recommendation - input 0. If you want to choose new random craft beer - input 1.") == '0'):
                            screen.fill((255, 228, 225))
                            ptext.draw(beer_recommender.main("test"), (0, 0), color=(0, 0, 128), fontsize=20)
                            pygame.display.update()
                            canOrGalss()
                        else:
                            beer = newbeer()
                            recMoney()

