import pygame
from player import Player
from platform import Platform
from enemy import Enemy
 
# Global constants
 
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BG_BLUE = (150, 200, 255)
 
# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Gift(pygame.sprite.Sprite):
    """ Klasa reprezentująca prezenty, które można zbierać podczas gry """

    def __init__(self, x, y, type_of):
        """ Konstruktor klasy Gift """

        super().__init__()

        if type_of == "Red":
            self.image = pygame.image.load("./obrazki/topdownTile_42.png").convert()
            self.image = self.image.subsurface((20,20,26,26))
            self.image = pygame.transform.scale(self.image, (30,30))
        elif type_of == "Blue":
            self.image = pygame.image.load("./obrazki/topdownTile_46.png").convert()
            self.image = self.image.subsurface((20,20,26,26))
            self.image = pygame.transform.scale(self.image, (30,30))
        elif type_of == "Green":
            self.image = pygame.image.load("./obrazki/topdownTile_50.png").convert()
            self.image = self.image.subsurface((20,20,26,26))
            self.image = pygame.transform.scale(self.image, (30,30))

        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.type = type_of

class Candy(pygame.sprite.Sprite):
    """ Klasa reprezentująca dźwignię otwierającą przejście do kolejnego poziomu """

    def __init__(self, x, y):
        """ Konstruktor klasy Candy """

        super().__init__()

        self.image = pygame.image.load("./obrazki/RTSobject_05.png").convert()
        self.image = self.image.subsurface((20,9,26,46))
        #self.image = pygame.transform.scale(self.image, (30,30))

        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.pushed = False

class Level(object):
    """ This is a generic super-class used to define a level.
        Create a child class for each level with level-specific
        info. """
 
    def __init__(self, player):
        """ Constructor. Pass in a handle to player. Needed for when moving platforms
            collide with the player. """
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.enemy_inbubble_list = pygame.sprite.Group()
        self.wall_list = pygame.sprite.Group()
        self.door_list = pygame.sprite.Group()
        self.gift_list = pygame.sprite.Group()
        self.lever_list = pygame.sprite.Group()
        self.player = player
         
        # Pozycja startowa gracza
        self.start = None

        # Choinka w tle
        self.tree = pygame.image.load("./obrazki/foliageTree_03.png").convert()
        self.tree = pygame.transform.scale(self.tree, (51,105))
        self.tree.set_colorkey(BLACK)

        # Pozycja choinki
        self.tree_pos = None
 
    # Update everything on this level
    def update(self):
        """ Update everything in this level."""
        self.wall_list.update()
        self.platform_list.update()
        self.enemy_list.update()
        self.enemy_inbubble_list.update()
 
    def draw(self, screen):
        """ Rysuje wszystkie elementy poziomu """
 
        # Tło
        screen.fill(BG_BLUE)
        screen.blit(self.tree, self.tree_pos)
 
        # Wszystko pozostałe zgromadzone w listach
        self.wall_list.draw(screen)
        self.door_list.draw(screen)
        self.platform_list.draw(screen)
        self.gift_list.draw(screen)
        self.lever_list.draw(screen)
        self.enemy_list.draw(screen)
 
def Platforma(x,y,ile_segmentow):
    if ile_segmentow == 1:
        return [40,20,x,y,2]
    elif ile_segmentow == 2:
        return [[40,20,x,y,2.1], [40,20,x+40,y,2.3]]
    else:
        p = []
        p.append([40,20,x,y,2.1])
        for i in range(ile_segmentow - 2):
            p.append([40,20,x+40*(i+1),y,2.2])
        p.append([40,20,x+40*(ile_segmentow - 1),y,2.3])
        return p

class Level_01(Level):
    """ Definition for level 1. """
 
    def __init__(self, player):
        """ Create level 1. """
 
        # Call the parent constructor
        Level.__init__(self, player)

        # Pozycja startowa gracza
        self.start = [50,100]

        # Choinka
        self.tree_pos = (695,145)
 
        # Array with width, height, x, and y of platform

        level = [*Platforma(40,450,5),
                 *Platforma(560,450,5),
                 *Platforma(560,250,5),
                 *Platforma(40,250,5),
                 *Platforma(300,350,5),
                 Platforma(120,150,1),
                 *Platforma(360,150,2),
                 Platforma(640,150,1)]
        #print(level)
 
        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1], platform[4])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)

        walls = []
        door = []
        seg_pion = int(SCREEN_HEIGHT/40)
        seg_poz = int(SCREEN_WIDTH/40)
        for i in range(seg_poz):
            walls.append([40, 40, 40*i, 0])			# sufit
            walls.append([40, 40, 40*i, SCREEN_HEIGHT - 40])	# podłoga
        for i in range(seg_pion):
            walls.append([40, 40, 0, 40*i])			# lewa ściana
        for i in range(8):
            walls.append([40, 40, SCREEN_WIDTH - 40, 40*i])	# prawa ściana
        for i in range(8,11):
            door.append([40, 40, SCREEN_WIDTH - 40, 40*i])
        for i in range(11,seg_pion):
            walls.append([40, 40, SCREEN_WIDTH - 40, 40*i])

        for platform in walls:
            wall = Platform(platform[0], platform[1], 1)
            wall.rect.x = platform[2]
            wall.rect.y = platform[3]
            wall.player = self.player
            self.wall_list.add(wall)

        for platform in door:
            wall = Platform(platform[0], platform[1], 1)
            wall.rect.x = platform[2]
            wall.rect.y = platform[3]
            wall.player = self.player
            self.door_list.add(wall)

        # Wrogowie z poziomu
        self.enemy_list.add(Enemy(80,300,1,"R"))
        self.enemy_list.add(Enemy(650,300,2,"L"))
        self.enemy_list.add(Enemy(680,100,3,"L"))

        # Prezenty
        self.gift_list.add(Gift(125,120,"Blue"))
        self.gift_list.add(Gift(645,220,"Red"))
        self.gift_list.add(Gift(85,530,"Green"))

        # Dźwignia
        self.lever_list.add(Candy(387,310))
        self.candy_pushed = [387,320]
        
class Level_02(Level):
    """ Definition for level 2. """
 
    def __init__(self, player):
        """ Create level 2. """
 
        # Call the parent constructor
        Level.__init__(self, player)

        # Pozycja startowa gracza
        self.start = [680,350]

        # Choinka
        self.tree_pos = (695,95)
 
        # Array with width, height, x, and y of platform

        level = [*Platforma(560,200,5),
                 Platforma(640,180,1),
                 *Platforma(360,300,4),
                 *Platforma(40,200,4),
                 Platforma(360,100,1)]
        #print(level)
 
        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1], platform[4])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)

        walls = []
        door = []
        seg_pion = int(SCREEN_HEIGHT/40)
        seg_poz = int(SCREEN_WIDTH/40)
        for i in range(2):
            walls.append([40, 40, 40*i, 0])			# sufit
            walls.append([40, 40, 40*i, SCREEN_HEIGHT - 40])
        for i in range(5,seg_poz):
            walls.append([40, 40, 40*i, 0])			# sufit
            walls.append([40, 40, 40*i, SCREEN_HEIGHT - 40])	# podłoga
        for i in range(seg_pion):
            walls.append([40, 40, 0, 40*i])			# lewa ściana
        for i in range(8):
            walls.append([40, 40, SCREEN_WIDTH - 40, 40*i])	# prawa ściana
        for i in range(8,11):
            door.append([40, 40, SCREEN_WIDTH - 40, 40*i])
        for i in range(11,seg_pion):
            walls.append([40, 40, SCREEN_WIDTH - 40, 40*i])
        walls.append([40, 40, 520, 40])
        walls.append([40, 40, 520, 180])
        walls.append([40, 40, 200, 520])
        walls.append([40, 40, 200, 480])

        for platform in walls:
            wall = Platform(platform[0], platform[1], 1)
            wall.rect.x = platform[2]
            wall.rect.y = platform[3]
            wall.player = self.player
            self.wall_list.add(wall)

        for platform in door:
            wall = Platform(platform[0], platform[1], 1)
            wall.rect.x = platform[2]
            wall.rect.y = platform[3]
            wall.player = self.player
            self.door_list.add(wall)

        # Wrogowie z poziomu
        self.enemy_list.add(Enemy(80,100,1,"R"))
        self.enemy_list.add(Enemy(600,300,2,"L"))
        self.enemy_list.add(Enemy(680,100,3,"L"))

        # Prezenty
        self.gift_list.add(Gift(365,70,"Blue"))
        #self.gift_list.add(Gift(645,220,"Red"))
        self.gift_list.add(Gift(45,530,"Green"))

        # Dźwignia
        self.lever_list.add(Candy(647,140))
        self.candy_pushed = [647,150]

class Level_03(Level):
    """ Definition for level 2. """
 
    def __init__(self, player):
        """ Create level 2. """
 
        # Call the parent constructor
        Level.__init__(self, player)

        # Pozycja startowa gracza
        self.start = [300,400]

        # Choinka
        self.tree_pos = (50,165)
 
        # Array with width, height, x, and y of platform

        level = [*Platforma(40,450,3),
                 *Platforma(260,360,3),
                 *Platforma(40,270,3),
                 *Platforma(260,180,3),
                 *Platforma(530,450,3),
                 *Platforma(420,340,2),
                 *Platforma(680,340,2),
                 *Platforma(550,250,2),
                 *Platforma(640,150,3)]
 
        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1], platform[4])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)

        walls = []
        door = []
        seg_pion = int(SCREEN_HEIGHT/40)
        seg_poz = int(SCREEN_WIDTH/40)
        for i in range(seg_poz):
            walls.append([40, 40, 40*i, 0])			# sufit
            walls.append([40, 40, 40*i, SCREEN_HEIGHT - 40])	# podłoga
        for i in range(seg_pion):
            walls.append([40, 40, 0, 40*i])			# lewa ściana
        for i in range(9):
            walls.append([40, 40, SCREEN_WIDTH - 40, 40*i])	# prawa ściana
        for i in range(9,12):
            door.append([40, 40, SCREEN_WIDTH - 40, 40*i])
        for i in range(12,seg_pion):
            walls.append([40, 40, SCREEN_WIDTH - 40, 40*i])
        for i in range(10):
            walls.append([40, 40, 380, 520 - 40*i])

        for platform in walls:
            wall = Platform(platform[0], platform[1], 1)
            wall.rect.x = platform[2]
            wall.rect.y = platform[3]
            wall.player = self.player
            self.wall_list.add(wall)

        for platform in door:
            wall = Platform(platform[0], platform[1], 1)
            wall.rect.x = platform[2]
            wall.rect.y = platform[3]
            wall.player = self.player
            self.door_list.add(wall)

        # Wrogowie z poziomu
        self.enemy_list.add(Enemy(50,150,1,"R"))
        self.enemy_list.add(Enemy(700,50,2,"L"))
        self.enemy_list.add(Enemy(430,450,3,"R"))

        # Prezenty
        self.gift_list.add(Gift(385,130,"Blue"))
        self.gift_list.add(Gift(570,220,"Red"))
        #self.gift_list.add(Gift(45,530,"Green"))

        # Dźwignia
        self.lever_list.add(Candy(70,409))
        self.candy_pushed = [70,419]