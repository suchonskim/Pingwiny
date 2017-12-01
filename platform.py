import pygame
from player import Player
 
# Global constants
 
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
 
# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Platform(pygame.sprite.Sprite):
    """ Platform the user can jump on """
 
    def __init__(self, width, height, type_of = 0):
        """ Platform constructor. Assumes constructed with user passing in
            an array of 5 numbers like what's defined at the top of this
            code. """
        super().__init__()
        
        if type_of == 0:
            self.image = pygame.Surface([width, height])
            self.image.fill(GREEN)
        elif type_of == 1:
            self.image = pygame.image.load("./obrazki/RTSobject_02.png").convert()
            self.image = pygame.transform.scale(self.image, (40,40))
        elif type_of == 2:
            self.image = pygame.image.load("./obrazki/tundraHalf.png").convert()
            self.image = pygame.transform.scale(self.image, (40,40))
            self.image = self.image.subsurface((0,0,40,20))
        elif type_of == 2.1:
            self.image = pygame.image.load("./obrazki/tundraHalfLeft.png").convert()
            self.image = pygame.transform.scale(self.image, (40,40))
            self.image = self.image.subsurface((0,0,40,20))
        elif type_of == 2.2:
            self.image = pygame.image.load("./obrazki/tundraHalfMid.png").convert()
            self.image = pygame.transform.scale(self.image, (40,40))
            self.image = self.image.subsurface((0,0,40,20))
        elif type_of == 2.3:
            self.image = pygame.image.load("./obrazki/tundraHalfRight.png").convert()
            self.image = pygame.transform.scale(self.image, (40,40))
            self.image = self.image.subsurface((0,0,40,20))
        self.image.set_colorkey(BLACK)
 
        self.rect = self.image.get_rect()
        self.collidable = [False,False,False,False]