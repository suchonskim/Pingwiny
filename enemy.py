import pygame
import random
 
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
 
def pingwinek(nr):
    if nr < 10:
        nazwa_pliku = "./obrazki/penguin_walk000" + str(nr) + ".png"
    else:
        nazwa_pliku = "./obrazki/penguin_walk00" + str(nr) + ".png"
    image = pygame.image.load(nazwa_pliku).convert()
    image = pygame.transform.scale(image, (51,58))
    image.set_colorkey(WHITE)
    return image

class Enemy(pygame.sprite.Sprite):
    """ Pingwinki - nasi wrogowie w grze """
 
    def __init__(self, x, y, nr, direction):
        """ Konstruktor klasy Enemy """
 
        super().__init__()

        self.walking_frames_l = []
        self.walking_frames_r = []

        self.direction = direction

        for i in range(16):
            image = pingwinek(i+1)
            self.walking_frames_r.append(image)
            image = pygame.transform.flip(image, True, False)
            self.walking_frames_l.append(image)

        self.image = self.walking_frames_r[0]
 
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
 
        # Prędkość pingwinków
        if self.direction == "R":
            self.change_x = 1
        else:
            self.change_x = -1
        self.change_y = 0

        self.level = None

        self.nr = nr

        self.update_pom = self.update

        self.in_bubble = False
        self.poczatek = 0
 
    def update(self):
        """ Wszelkie akcje wykonywane przez pingwinka """
        # Grawitacja
        self.calc_grav()

        # Jeśli jest ponad platformą, to może na nią wskoczyć
        for block in self.level.platform_list:
            if self.rect.bottom < block.rect.top:
                block.collidable[self.nr] = True

        # Zawracanie w losowym momencie (średnio raz na 15 sekund)
        los = random.randint(1,450)
        if los == 243:
            self.change_x *= -1
            if self.direction == "R":
                self.direction = "L"
            else:
                self.direction = "R"
 
        # Ruch w poziomie
        self.rect.x += self.change_x

        pos = self.rect.x
        if self.direction == "R":
            frame = (pos // 3) % len(self.walking_frames_r)
            self.image = self.walking_frames_r[frame]
        else:
            frame = (pos // 3) % len(self.walking_frames_l)
            self.image = self.walking_frames_l[frame]
 
        # Zderzenia ze ścianami w poziomie
        wall_hit_list = pygame.sprite.spritecollide(self, self.level.wall_list, False)
        for wall in wall_hit_list:
            if self.change_x > 0:
                self.rect.right = wall.rect.left
                self.direction = "L"
            elif self.change_x < 0:
                self.rect.left = wall.rect.right
                self.direction = "R"
        if len(wall_hit_list) > 0:	# Po uderzeniu w ścianę ma zawrócić
            self.change_x *= -1

        door_hit_list = pygame.sprite.spritecollide(self, self.level.door_list, False)
        for wall in door_hit_list:
            if self.change_x > 0:
                self.rect.right = wall.rect.left
                self.direction = "L"
            elif self.change_x < 0:
                self.rect.left = wall.rect.right
                self.direction = "R"
        if len(door_hit_list) > 0:	# Po uderzeniu w ścianę ma zawrócić
            self.change_x *= -1

        # Skakanie w losowym momencie (średnio raz na 7 sekund)
        los = random.randint(1,210)
        if los == 42:
            self.jump()
 
        # Ruch w pionie
        self.rect.y += self.change_y
 
        # Zderzenia ze ścianami w pionie (podłoga, sufit)
        wall_hit_list = pygame.sprite.spritecollide(self, self.level.wall_list, False)
        for wall in wall_hit_list:
            if self.change_y > 0:
                self.rect.bottom = wall.rect.top
                self.change_y = 0
            elif self.change_y < 0:
                self.rect.top = wall.rect.bottom

            self.change_y = 0

        for block in self.level.platform_list:
            if self.rect.right > block.rect.left and \
               self.rect.left < block.rect.right and \
               block.collidable[self.nr] == True and \
               self.rect.bottom >= block.rect.top:
                self.rect.bottom = block.rect.top
                self.change_y = 0

        for block in self.level.platform_list:
            if self.rect.bottom > block.rect.top:
                block.collidable[self.nr] = False
 
    def calc_grav(self):
        """ Metoda, która dodaje efekt grawitacji """
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35
 
    def jump(self):
        """ Podskakiwanie pingwinka """
 
        self.rect.y += 18
        wybicie = 0
        for platform in self.level.platform_list:
            if (pygame.sprite.collide_rect(self, platform) and self.rect.bottom <= platform.rect.bottom):
                wybicie += 1
        self.rect.y -= 18
 
        # Skacze wtedy, kiedy ma się z czego wybić
        if wybicie > 0 or self.rect.bottom >= SCREEN_HEIGHT -40:
            self.change_y = -10

    def grav_upside_down(self):
        """ Unoszenie """
        if self.change_y >= 0:
            self.change_y = -0.3
        else:
            self.change_y -= 0.15

    def bub_update(self):
        """ Co się dzieje z pingwinkiem zamkniętym w bańce """
        self.grav_upside_down()
 
        # Ruch w pionie
        self.rect.y += self.change_y
 
        # Zderzenia ze ścianami w pionie (podłoga, sufit)
        wall_hit_list = pygame.sprite.spritecollide(self, self.level.wall_list, False)
        for wall in wall_hit_list:
            if self.change_y > 0:
                self.rect.bottom = wall.rect.top
                self.change_y = 0
            elif self.change_y < 0:
                self.rect.top = wall.rect.bottom
 
            self.change_y = 0

        if self.rect.top < 0:
            self.rect.top = 0
            self.change_y = 0

    def bubble(self):
        """ Metoda wywoływana, gdy pingwinek zostanie trafiony bąbelkiem """

        self.in_bubble = True
        self.level.enemy_inbubble_list.add(self)
        self.poczatek = pygame.time.get_ticks()

        # Obrazek pingwinka w bańce
        bubble = pygame.image.load("./obrazki/bubble.png").convert()
        bubble = bubble.subsurface((0,0,32,32))
        bubble = pygame.transform.scale(bubble, (50,50))
        bubble.set_colorkey(BLACK)
        bubble.set_alpha(90)

        self.image = pygame.image.load("./obrazki/penguin_jump.png").convert()
        self.image = pygame.transform.scale(self.image, (51,58))
        self.image.set_colorkey(WHITE)
        self.image.blit(bubble, (0,0))

        # Co się dzieje z pingwinkiem
        self.update = self.bub_update

    def unbubble(self):
        """ Jeśli nie uda nam się przebić bąbelka w określonym czasie, to pingwinek się z niego wydostaje """
        self.in_bubble = False
        self.level.enemy_inbubble_list.remove(self)
        self.update = self.update_pom
