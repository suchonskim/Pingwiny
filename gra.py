#!/opt/anaconda/bin/python3
# coding: utf-8

# In[ ]:


import pygame
from player import Player
from platform import Platform
from levels import Level, Level_01, Level_02, Level_03
 
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
 
 
def main():
    """ Main Program """
    pygame.init()
 
    # Set the height and width of the screen
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
 
    pygame.display.set_caption("Pingwiny z Rovaniemi")
 
    # Create the player
    player = Player()
 
    # Create all the levels
    level_list = []
    level_list.append( Level_01(player) )
    level_list.append( Level_02(player) )
    level_list.append( Level_03(player) )
 
    # Set the current level
    current_level_no = 0
    current_level = level_list[current_level_no]
 
    active_sprite_list = pygame.sprite.Group()
    player.level = current_level
    for enemy in current_level.enemy_list:
        enemy.level = current_level
 
    player.rect.x = player.level.start[0]
    player.rect.y = player.level.start[1]
    active_sprite_list.add(player)

    bubble_list = pygame.sprite.Group()

    # Wczytujemy aktualny najlepszy wynik
    high_score_file = open("high_score.txt", "r")
    high_score_str = high_score_file.readlines()
    high_score = [int(high_score_str[0]),int(high_score_str[1])]
    high_score_file.close()

    font = pygame.font.Font(None, 45)
    timerfont = pygame.font.Font(None, 40)
    titlefont = pygame.font.Font(None, 60)

    frame_count = 0
    minutes = 0
    seconds = 0

    game_over = False
    win_game = False
 
    # Loop until the user clicks the close button.
    done = False
 
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    display_menu = True
    display_instructions = False
    option = 0

    # Odczytywanie ustawień z pliku
    settings_file = open("settings.txt", "r")
    settings_str = settings_file.readlines()
    settings = [int(settings_str[0]),int(settings_str[1])]
    settings_file.close()

    difficulty = settings[0]
    mute = settings[1]

    # -------- Main menu Loop -----------
    while not done and display_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    option +=1
                    option = option % 5
                if event.key == pygame.K_UP:
                    option -=1
                    option = option % 5
                if display_instructions == True and event.key == pygame.K_SPACE:
                    display_instructions = False
                if event.key == pygame.K_RETURN and option == 0:
                    display_menu = False
                if event.key == pygame.K_RETURN and option == 1:
                    display_instructions = True
                if event.key == pygame.K_RETURN and option == 2:
                    difficulty += 1
                    difficulty = difficulty % 3
                if event.key == pygame.K_RETURN and option == 3:
                    mute *= -1
                if event.key == pygame.K_RETURN and option == 4:
                    done = True
 
        # Set the screen background
        screen.fill(BG_BLUE)
        wall_list = pygame.sprite.Group()
        walls = []
        seg_pion = int(SCREEN_HEIGHT/40)
        seg_poz = int(SCREEN_WIDTH/40)
        for i in range(seg_poz):
            walls.append([40, 40, 40*i, 0])			# sufit
            walls.append([40, 40, 40*i, SCREEN_HEIGHT - 40])	# podłoga
        for i in range(seg_pion):
            walls.append([40, 40, 0, 40*i])			# lewa ściana
            walls.append([40, 40, SCREEN_WIDTH - 40, 40*i])	# prawa ściana

        for platform in walls:
            wall = Platform(platform[0], platform[1], 1)
            wall.rect.x = platform[2]
            wall.rect.y = platform[3]
            wall_list.add(wall)
        wall_list.draw(screen)
 
        if display_instructions == True:

            ster = titlefont.render("Sterowanie", True, BLUE)
            ster_rect = ster.get_rect()
            ster_x = SCREEN_WIDTH / 2 - ster_rect.width / 2
            screen.blit(ster, [ster_x, 80])
 
            up = pygame.image.load("./obrazki/Keyboard_Black_Arrow_Up.png").convert()
            up = pygame.transform.scale(up, (50,50))
            up.set_colorkey(BLACK)
            screen.blit(up, [200, 350])

            up_ins = font.render("Skok", True, BLACK)
            screen.blit(up_ins, [300, 360])

            left = pygame.image.load("./obrazki/Keyboard_Black_Arrow_Left.png").convert()
            left = pygame.transform.scale(left, (50,50))
            left.set_colorkey(BLACK)
            screen.blit(left, [200, 250])

            left_ins = font.render("Ruch w lewo", True, BLACK)
            screen.blit(left_ins, [300, 260])

            right = pygame.image.load("./obrazki/Keyboard_Black_Arrow_Right.png").convert()
            right = pygame.transform.scale(right, (50,50))
            right.set_colorkey(BLACK)
            screen.blit(right, [200, 150])

            right_ins = font.render("Ruch w prawo", True, BLACK)
            screen.blit(right_ins, [300, 160])

            space = pygame.image.load("./obrazki/Keyboard_Black_Space.png").convert()
            space = pygame.transform.scale(space, (50,50))
            space.set_colorkey(BLACK)
            screen.blit(space, [200, 450])

            space_ins = font.render("Strzał bąbelkiem", True, BLACK)
            screen.blit(space_ins, [300, 460])

            powrot = font.render("Jeśli chcesz wrócić do Menu, wciśnij SPACJĘ", True, WHITE)
            powrot_rect = powrot.get_rect()
            powrot_x = SCREEN_WIDTH / 2 - powrot_rect.width / 2
            screen.blit(powrot, [powrot_x, 520])

        else:
            nazwa = titlefont.render("Pingwiny z Rovaniemi", True, BLACK)
            nazwa_rect = nazwa.get_rect()
            nazwa_x = SCREEN_WIDTH / 2 - nazwa_rect.width / 2
            screen.blit(nazwa, [nazwa_x, 80])

            start = font.render("Start Gry", True, BLACK)
            sterowanie = font.render("Sterowanie", True, BLACK)
            poziom_trudnosci = font.render("Poziom Trudności", True, BLACK)
            dzwiek = font.render("Dźwięk", True, BLACK)
            wyjscie = font.render("Wyjście", True, BLACK)

            if option == 0:
                start = font.render("Start Gry", True, BLUE)
            elif option == 1:
                sterowanie = font.render("Sterowanie", True, BLUE)
            elif option == 2:
                if difficulty == 0:
                    poziom_trudnosci = font.render("Poziom Trudności: Łatwy", True, BLUE)
                elif difficulty == 1:
                    poziom_trudnosci = font.render("Poziom Trudności: Średni", True, BLUE)
                else:
                    poziom_trudnosci = font.render("Poziom Trudności: Trudny", True, BLUE)
            elif option == 3:
                if mute == -1:
                    dzwiek = font.render("Dźwięk: włączony", True, BLUE)
                else:
                    dzwiek = font.render("Dźwięk: wyłączony", True, BLUE)
            else:
                wyjscie = font.render("Wyjście", True, BLUE)

            start_rect = start.get_rect()
            start_x = SCREEN_WIDTH / 2 - start_rect.width / 2
            screen.blit(start, [start_x, 170])

            sterowanie_rect = sterowanie.get_rect()
            sterowanie_x = SCREEN_WIDTH / 2 - sterowanie_rect.width / 2
            screen.blit(sterowanie, [sterowanie_x, 230])

            poziom_trudnosci_rect = poziom_trudnosci.get_rect()
            poziom_trudnosci_x = SCREEN_WIDTH / 2 - poziom_trudnosci_rect.width / 2
            screen.blit(poziom_trudnosci, [poziom_trudnosci_x, 290])

            dzwiek_rect = dzwiek.get_rect()
            dzwiek_x = SCREEN_WIDTH / 2 - dzwiek_rect.width / 2
            screen.blit(dzwiek, [dzwiek_x, 350])

            wyjscie_rect = wyjscie.get_rect()
            wyjscie_x = SCREEN_WIDTH / 2 - wyjscie_rect.width / 2
            screen.blit(wyjscie, [wyjscie_x, 410])

            naw = font.render("Nawigacja strzałkami góra/dół", True, WHITE)
            naw_rect = naw.get_rect()
            naw_x = SCREEN_WIDTH / 2 - naw_rect.width / 2
            screen.blit(naw, [naw_x, 480])

            naw2 = font.render("Wybór/zmiana przyciskiem ENTER", True, WHITE)
            naw2_rect = naw2.get_rect()
            naw2_x = SCREEN_WIDTH / 2 - naw2_rect.width / 2
            screen.blit(naw2, [naw2_x, 520])
 
        clock.tick(60)
 
        pygame.display.flip()

    for enemy in current_level.enemy_list:
        if enemy.direction == "R":
            enemy.change_x = 1 + 0.5*difficulty
        else:
            enemy.change_x = -1 - 0.5*difficulty

    # Dźwięki
    pop = pygame.mixer.Sound("./dzwieki/pop.ogg")
    santa = pygame.mixer.Sound("./dzwieki/santa-ho-ho-ho-2.ogg")
    switch = pygame.mixer.Sound("./dzwieki/switch5.ogg")

    # Wyciszenie
    if mute == 1:
        pop.set_volume(0)
        santa.set_volume(0)
        switch.set_volume(0)

    # Zapisanie ustawień
    settings_file = open("settings.txt", "w")
    settings_file.writelines([str(difficulty)+"\n",str(mute)])
    settings_file.close()

    # -------- Main Program Loop -----------
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.go_left()
                if event.key == pygame.K_RIGHT:
                    player.go_right()
                if event.key == pygame.K_UP:
                    player.jump()
                if event.key == pygame.K_SPACE:
                    bubble = player.bubble()
                    bubble.level = current_level
                    active_sprite_list.add(bubble)
                    bubble_list.add(bubble)
                    if player.direction == "R":
                        bubble.where_pop = bubble.rect.x + bubble.range + player.bonus - 50*difficulty
                    else:
                        bubble.where_pop = player.rect.x - bubble.range - player.bonus + 50*difficulty

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.change_x < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT and player.change_x > 0:
                    player.stop()
 
        # Update the player and bubbles
        active_sprite_list.update()
 
        # Update items in the level
        current_level.update()
 
        # Zmiana poziomu przy przejściu przez drzwi
        if player.rect.left > SCREEN_WIDTH:
            current_level_no += 1
            if current_level_no == 3:
                win_game = True
                done = True
            else:
                current_level = level_list[current_level_no]
                active_sprite_list = pygame.sprite.Group()
                player.level = current_level
                current_level.difficulty = difficulty
                for enemy in current_level.enemy_list:
                    enemy.level = current_level
 
            player.rect.x = player.level.start[0]
            player.rect.y = player.level.start[1]
            active_sprite_list.add(player)

            bubble_list = pygame.sprite.Group()

        # Kiedy gracz wskoczy w podłogę, to pojawia się na suficie
        if player.rect.top > SCREEN_HEIGHT:
            player.rect.bottom = 0

        # To samo dla pingwinków
        for enemy in current_level.enemy_list:
            if enemy.rect.top > SCREEN_HEIGHT:
                enemy.rect.bottom = 0

        for bubble in bubble_list:
 
            # Wrogowie trafieni bąbelkiem
            enemy_hit_list = pygame.sprite.spritecollide(bubble, current_level.enemy_list, False)
 
            # Jak trafiliśmy wroga, to bąbelek znika
            if len(enemy_hit_list) > 0:
                bubble_list.remove(bubble)
                active_sprite_list.remove(bubble)

            for enemy in enemy_hit_list:
                enemy.bubble()

            wall_hit_list = pygame.sprite.spritecollide(bubble, current_level.wall_list, False)
 
            # Bąbelek pęka po zderzeniu ze ścianą
            if len(wall_hit_list) > 0:
                pop.play()
                bubble_list.remove(bubble)
                active_sprite_list.remove(bubble)

            # Bąbelek znika gdy za długo leci
            if ((player.direction == "R" and bubble.rect.x > bubble.where_pop) or (player.direction == "L" and bubble.rect.x + bubble.rect.width < bubble.where_pop)):
                pop.play()
                bubble_list.remove(bubble)
                active_sprite_list.remove(bubble)

        for enemy in current_level.enemy_inbubble_list:
            # Wydostanie się z bąbelka
            koniec = pygame.time.get_ticks()
            if koniec - enemy.poczatek > (7000 - 1000*difficulty):
                pop.play()
                enemy.unbubble()
            elif (player.rect.right > enemy.rect.left - 2) and (player.rect.left < enemy.rect.right + 2) and (player.rect.top < enemy.rect.bottom + 2) and (player.rect.bottom > enemy.rect.top - 2):
                pop.play()
                current_level.enemy_list.remove(enemy)
                current_level.enemy_inbubble_list.remove(enemy)

        gifts_collected = pygame.sprite.spritecollide(player,current_level.gift_list,True)
        for gift in gifts_collected:
            if gift.type == "Blue":
                santa.play()
            elif gift.type == "Green":
                player.bonus += 100
            elif gift.type == "Red":
                player.speed += 2

        lever_pushed = pygame.sprite.spritecollide(player, current_level.lever_list,False)
        if len(lever_pushed) > 0 and len(current_level.enemy_list) == 0:
            for candy in current_level.lever_list:
                if candy.pushed == False:
                    switch.play()
                    candy.image = pygame.image.load("./obrazki/RTSobject_10.png").convert()
                    candy.image = candy.image.subsurface((12,16,41,30))
                    candy.image.set_colorkey(BLACK)
                    candy.rect = candy.image.get_rect()
                    candy.rect.x = current_level.candy_pushed[0]
                    candy.rect.y = current_level.candy_pushed[1]
                    candy.pushed = True
                    current_level.door_list.empty()

        if player.dead:
            done = True
            game_over = True

        total_seconds = frame_count // 30
 
        # Divide by 60 to get total minutes
        minutes = total_seconds // 60
 
        # Use modulus (remainder) to get seconds
        seconds = total_seconds % 60
 
        # Use python string formatting to format in leading zeros
        output_string = "Czas: {0:02}:{1:02}".format(minutes, seconds)

        current_level.draw(screen)
        active_sprite_list.draw(screen)
 
        # Blit to the screen
        text = timerfont.render(output_string, True, BLUE)
        screen.blit(text, [80, 10])

        frame_count += 1
 
        clock.tick(30)
 
        pygame.display.flip()

    quit = False
    while game_over and not quit:
        screen.fill(BG_BLUE)

        wall_list = pygame.sprite.Group()
        walls = []
        seg_pion = int(SCREEN_HEIGHT/40)
        seg_poz = int(SCREEN_WIDTH/40)
        for i in range(seg_poz):
            walls.append([40, 40, 40*i, 0])			# sufit
            walls.append([40, 40, 40*i, SCREEN_HEIGHT - 40])	# podłoga
        for i in range(seg_pion):
            walls.append([40, 40, 0, 40*i])			# lewa ściana
            walls.append([40, 40, SCREEN_WIDTH - 40, 40*i])	# prawa ściana

        for platform in walls:
            wall = Platform(platform[0], platform[1], 1)
            wall.rect.x = platform[2]
            wall.rect.y = platform[3]
            wall_list.add(wall)
        wall_list.draw(screen)

        koniec = font.render("Koniec gry", True, BLUE)
        koniec_rect = koniec.get_rect()
        koniec_x = SCREEN_WIDTH / 2 - koniec_rect.width / 2
        koniec_y = SCREEN_HEIGHT / 2 - koniec_rect.height / 2

        screen.blit(koniec, [koniec_x, koniec_y])

        powrot = font.render("Jeśli chcesz zagrać jeszcze raz, wciśnij SPACJĘ", True, WHITE)
        powrot_rect = powrot.get_rect()
        powrot_x = SCREEN_WIDTH / 2 - powrot_rect.width / 2
        screen.blit(powrot, [powrot_x, 520])

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    main()

    quit = False
    current_score = [minutes,seconds]
    while win_game and not quit:
        screen.fill(BG_BLUE)

        wall_list = pygame.sprite.Group()
        walls = []
        seg_pion = int(SCREEN_HEIGHT/40)
        seg_poz = int(SCREEN_WIDTH/40)
        for i in range(seg_poz):
            walls.append([40, 40, 40*i, 0])			# sufit
            walls.append([40, 40, 40*i, SCREEN_HEIGHT - 40])	# podłoga
        for i in range(seg_pion):
            walls.append([40, 40, 0, 40*i])			# lewa ściana
            walls.append([40, 40, SCREEN_WIDTH - 40, 40*i])	# prawa ściana

        for platform in walls:
            wall = Platform(platform[0], platform[1], 1)
            wall.rect.x = platform[2]
            wall.rect.y = platform[3]
            wall_list.add(wall)
        wall_list.draw(screen)

        grat = font.render("Gratulacje!", True, BLUE)
        grat_rect = grat.get_rect()
        grat_x = SCREEN_WIDTH / 2 - grat_rect.width / 2
        grat_y = SCREEN_HEIGHT / 2 - grat_rect.height / 2

        output_string = "{0:01}:{1:02}".format(minutes, seconds)
        czas = font.render("Twój czas to: " + output_string, True, BLUE)
        czas_rect = czas.get_rect()
        czas_x = SCREEN_WIDTH / 2 - czas_rect.width / 2
        czas_y = SCREEN_HEIGHT / 2 - czas_rect.height / 2 + 40

        if current_score[0] < high_score[0] or (current_score[0] == high_score[0] and current_score[1] < high_score[1]):
            high = font.render("Pobiłeś rekord!", True, BLUE)
            high_score_file = open("high_score.txt", "w")
            high_score_file.writelines([str(current_score[0])+"\n",str(current_score[1])])
            high_score_file.close()
        else:
            high = font.render("Aktualny rekord to: " + str(high_score[0]) + ":" + str(high_score[1]), True, BLUE)

        high_rect = high.get_rect()
        high_x = SCREEN_WIDTH / 2 - high_rect.width / 2
        high_y = SCREEN_HEIGHT / 2 - high_rect.height / 2 + 80

        screen.blit(grat, [grat_x, grat_y])
        screen.blit(czas, [czas_x, czas_y])
        screen.blit(high, [high_x, high_y])

        powrot = font.render("Jeśli chcesz zagrać jeszcze raz, wciśnij SPACJĘ", True, WHITE)
        powrot_rect = powrot.get_rect()
        powrot_x = SCREEN_WIDTH / 2 - powrot_rect.width / 2
        screen.blit(powrot, [powrot_x, 520])

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    main()
 
    pygame.quit()
 
if __name__ == "__main__":
    main()

