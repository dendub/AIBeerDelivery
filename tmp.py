






import random, time
import sys, pygame
import numpy as np

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
    home = pygame.image.load("media/home.png")
    agent = pygame.image.load("media/agent2.png")
    warehouse = pygame.image.load("media/warehouse.png")
    step = pygame.image.load("media/step.png")
    gridrect = agent.get_rect()
    homerect = home.get_rect()
    agentrect = agent.get_rect()
    warehouserect = warehouse.get_rect()
    steprect = step.get_rect()
    w, h = gridrect.width, gridrect.height

    size = width, height = len(map[0])*w, len(map)*h
    screen = pygame.display.set_mode(size)

    for s, ns in zip(steps[0: -1], steps[1:]):
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




    # agentrect.center = ((steps[0][1])*w + w/2, (steps[0][0])*h+h/2)
    # screen.blit(agent, agentrect)

        warehouserect.center = ((steps[-1][1])*w + w/2, (steps[-1][0])*h+h/2)
        screen.blit(warehouse, warehouserect)



        agentrect.center = ((s[1])*w + w/2, (s[0])*h+h/2)

        newdir = direction(s, ns)

        screen.blit(pygame.transform.rotate(agent, 90*newdir), agentrect)
        pygame.display.flip()
        time.sleep(1)


    # while(True):
    #         for event in pygame.event.get():
    #             if event.type == pygame.QUIT: sys.exit()
