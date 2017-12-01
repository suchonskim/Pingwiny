import pygame
 
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
 
def bieg_obrazek(nr):
    """ Funkcja do ładowania obrazków Mikołaja biegnącego """
    nazwa_pliku = "./obrazki/Run (" + str(nr) + ").png"
    image = pygame.image.load(nazwa_pliku).convert()
    image = image.subsurface((210,30,360,550))
    image = pygame.transform.scale(image, (52,80))
    image.set_colorkey(BLACK)
    return image

def skok_obrazek(nr):
    """ Funkcja do ładowania obrazków Mikołaja skaczącego """
    nazwa_pliku = "./obrazki/Jump (" + str(nr) + ").png"
    image = pygame.image.load(nazwa_pliku).convert()
    image = image.subsurface((120,45,480,550))
    image = pygame.transform.scale(image, (70,80))
    image.set_colorkey(BLACK)
    return image

class Bubble(pygame.sprite.Sprite):
    """ Klasa reprezentująca bąbelki, którymi walczymy z wrogami """

    def __init__(self, x, y):
        """ Konstruktor bąbelków """
        
        super().__init__()

        self.image = pygame.image.load("./obrazki/bubble.png").convert()
        self.image = self.image.subsurface((0,0,32,32))
        self.image = pygame.transform.scale(self.image, (60,60))
        self.image.set_colorkey(BLACK)
        self.image.set_alpha(90)

        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

        self.change_x = 7
        self.change_y = 0

        self.level = None

        # Jak daleko może polecieć
        self.range = 200
        self.where_pop = 0

    def update(self):
        self.rect.x += self.change_x

class Player(pygame.sprite.Sprite):
    """ Postać Świętego Mikołaja - bohater, którym porusza się gracz """

    def __init__(self):
        """ Konstruktor klasy Player """
 
        super().__init__()

        # Listy obrazków Mikołaja biegnącego w lewo i w prawo oraz skaczącego
        self.walking_frames_l = []
        self.walking_frames_r = []
        self.jumping_frames_l = []
        self.jumping_frames_r = []
 
        # W którym kierunku się patrzy (R - w prawo, L - w lewo)
        self.direction = "R"

        # Ładujemy obrazek stojącego Mikołaja obróconego w prawo
        image = pygame.image.load("./obrazki/Idle(1).png").convert()
        image = image.subsurface((180,30,360,550))
        image = pygame.transform.scale(image, (52,80))
        image.set_colorkey(BLACK)
        self.standing_frame_r = image
        # I stojący w lewo
        image = pygame.transform.flip(image, True, False)
        self.standing_frame_l = image

        # Ładujemy obrazki do biegania
        for i in range(11):
            image = bieg_obrazek(i+1)
            self.walking_frames_r.append(image)
            image = pygame.transform.flip(image, True, False)
            self.walking_frames_l.append(image)

        # Ładujemy obrazki do skakania
        for i in range(15):
            image = skok_obrazek(i+1)
            self.jumping_frames_r.append(image)
            image = pygame.transform.flip(image, True, False)
            self.jumping_frames_l.append(image)

        self.image = self.walking_frames_r[0]
        self.rect = self.image.get_rect()
 
        # Prędkość w poziomie i w pionie
        self.change_x = 0
        self.change_y = 0
 
        # Lista obiektów na danym poziomie, na które można wpaść
        self.level = None

        # Dodatkowy zasięg bąbelków
        self.bonus = 0

        # Dodatkowe przyspieszenie
        self.speed = 0

        # Czy umarł
        self.dead = False
 
    def update(self):
        """ Akcje podejmowane przez gracza """
        # Grawitacja
        self.calc_grav()

        for block in self.level.platform_list:
            if self.rect.bottom < block.rect.top:
                block.collidable[0] = True
 
        # Ruch w poziomie
        self.rect.x += self.change_x

        pos = self.rect.x
        if self.direction == "R":
            if self.change_x > 0:
                frame = (pos // 20) % len(self.walking_frames_r)
                self.image = self.walking_frames_r[frame]
            else:
                self.image = self.standing_frame_r
        else:
            if self.change_x < 0:
                frame = (pos // 20) % len(self.walking_frames_l)
                self.image = self.walking_frames_l[frame]
            else:
                self.image = self.standing_frame_l
 
        # Zderzenia ze ścianami w poziomie
        wall_hit_list = pygame.sprite.spritecollide(self, self.level.wall_list, False)
        for wall in wall_hit_list:
            if self.change_x > 0:
                self.rect.right = wall.rect.left
            elif self.change_x < 0:
                self.rect.left = wall.rect.right

        door_hit_list = pygame.sprite.spritecollide(self, self.level.door_list, False)
        for wall in door_hit_list:
            if self.change_x > 0:
                self.rect.right = wall.rect.left
            elif self.change_x < 0:
                self.rect.left = wall.rect.right

        # Zderzenia z wrogami
        enemy_hit_list = pygame.sprite.spritecollide(self, self.level.enemy_list, False)
        
        for enemy in enemy_hit_list:
            if enemy.in_bubble:
                enemy_hit_list.remove(enemy)
            if self.change_x > 0:
                self.rect.right = enemy.rect.left
            elif self.change_x < 0:
                self.rect.left = enemy.rect.right
            elif enemy.change_x > 0:	# Kiedy to przeciwnik na nas wpadnie
                self.rect.left = enemy.rect.right
            else:
                self.rect.right = enemy.rect.left
        if len(enemy_hit_list) > 0:
            self.dead = True
            print("Zabity")
 
        # Ruch w pionie
        self.rect.y += self.change_y

        pos = self.rect.y
        if self.direction == "R" and self.change_y < 0:
            frame = (pos // 20) % len(self.jumping_frames_r)
            self.image = self.jumping_frames_r[frame]
        elif self.direction == "L" and self.change_y < 0:
            frame = (pos // 20) % len(self.jumping_frames_l)
            self.image = self.jumping_frames_l[frame]
 
        # Zderzenia ze ścianami w pionie (podłoga, sufit)
        wall_hit_list = pygame.sprite.spritecollide(self, self.level.wall_list, False)
        for wall in wall_hit_list:
            if self.change_y > 0:
                self.rect.bottom = wall.rect.top
            elif self.change_y < 0:
                self.rect.top = wall.rect.bottom
            self.change_y = 0

        for block in self.level.platform_list:
            if self.rect.right > block.rect.left and \
               self.rect.left < block.rect.right and \
               block.collidable[0] == True and \
               self.rect.bottom >= block.rect.top:
                self.rect.bottom = block.rect.top
                self.change_y = 0

        for block in self.level.platform_list:
            if self.rect.bottom > block.rect.top:
                block.collidable[0] = False

        # Zderzenia z wrogami
        enemy_hit_list = pygame.sprite.spritecollide(self, self.level.enemy_list, False)

        for enemy in enemy_hit_list:
            if enemy.in_bubble:
                enemy_hit_list.remove(enemy)
            if self.change_y > 0:
                self.rect.bottom = enemy.rect.top
                self.change_y = 0
            elif self.change_y < 0:
                self.rect.top = enemy.rect.bottom
            elif enemy.change_y > 0:	# Kiedy to przeciwnik na nas wpadnie
                self.rect.top = enemy.rect.bottom
            else:
                self.rect.bottom = enemy.rect.top
            self.change_y = 0
        if len(enemy_hit_list) > 0:
            self.dead = True
            print("Zabity")
 
    def calc_grav(self):
        """ Dodaje efekt grawitacji """
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35
 
    def jump(self):
        """ Skakanie (po wciśnięciu strzałki w górę) """

        self.rect.y += 2
        wybicie = 0
        for platform in self.level.platform_list:
            if (pygame.sprite.collide_rect(self, platform) and self.rect.bottom <= platform.rect.top+2):
                wybicie += 1
        for wall in self.level.wall_list:
            if (pygame.sprite.collide_rect(self, wall) and self.rect.bottom <= wall.rect.top+2):
                wybicie += 1
        self.rect.y -= 2
 
        # Skacze gdy ma z czego się wybić
        if wybicie > 0 or self.rect.bottom >= SCREEN_HEIGHT -40:
            self.change_y = -10
 
    # Ruch sterowany strzałkami:
    def go_left(self):
        """ Ruch w lewo (po wciśnięciu strzałki w lewo) """
        self.change_x = -6 - self.speed
        self.direction = "L"
 
    def go_right(self):
        """ Ruch w prawo (po wciśnięciu strzałki w prawo) """
        self.change_x = 6 + self.speed
        self.direction = "R"
 
    def stop(self):
        """ Zatrzymanie się (gdy gracz przestanie wciskać strzałki) """
        self.change_x = 0

    def bubble(self):
        """ Strzelanie bąbelkami (po wciśnięciu spacji) """
        if self.direction == "R":
            bubble = Bubble(self.rect.x + self.rect.width, self.rect.y + 10)
            bubble.change_x = 7
        else:
            bubble = Bubble(self.rect.x - 60, self.rect.y + 10)
            bubble.change_x = -7
        return bubble