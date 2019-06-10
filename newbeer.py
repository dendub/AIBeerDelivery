from textgenrnn import textgenrnn
import pygame
import time
textgen = textgenrnn(weights_path='newbeer/colaboratory_weights.hdf5',
                       vocab_path='newbeer/colaboratory_vocab.json',
                       config_path='newbeer/colaboratory_config.json')

# textgen.generate_samples(max_gen_length=20, temperature=0.8)
textgen.generate_to_file('newbeer/textgenrnn_texts.txt', max_gen_length=3, temperature=3)

f=open("newbeer/textgenrnn_texts.txt", "r")

for l in f:
    texts = l



pygame.init()
beer = pygame.image.load("newbeer/beer.png")
beerrect = beer.get_rect()

texts = texts.replace('\n', '').split(' ')
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
