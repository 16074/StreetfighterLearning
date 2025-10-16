import pygame
from pygame import mixer

pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.init()

clock = pygame.time.Clock()
fps = 60

screen = pygame.display.set_mode((928, 704))
pygame.display.set_caption("Platformer")

#lettertype definiëren
font = pygame.font.SysFont('Bauhaus 93', 40)
font_score = pygame.font.SysFont('Bauhaus 93', 16)

#variabelen voor de game
tile_size = 32
game_over = 0
main_menu = True
level = 1
max_levels = 5
score = 0

#kleuren definiëren
white = (255, 255, 255)

#afbeeldingen laden
achtergrond_img = pygame.image.load('achtergrond_p.png')
achtergrond_boss_img = pygame.image.load('achtergrond_boss.png')
grond_img = pygame.image.load('grond.png')
gras_img = pygame.image.load('gras.png')
restart_img = pygame.image.load('restart.png')
play_img = pygame.image.load('play.png')
stop_img = pygame.image.load('stop.png')

#geluiden laden
pygame.mixer.music.load('bg_music.mp3')
pygame.mixer.music.play(-1, 0.0, 5000)
coin_fx = pygame.mixer.Sound('coin.mp3')
coin_fx.set_volume(0.5)
jump_fx = pygame.mixer.Sound('jump.mp3')
jump_fx.set_volume(0.5)
dead_fx = pygame.mixer.Sound('dood.mp3')
dead_fx.set_volume(0.5)
victory_fx = pygame.mixer.Sound('victory.mp3')
victory_fx.set_volume(0.5)

#tekst laden
def draw_text(text, font, text_colour, x, y):
    img = font.render(text, True, text_colour)
    screen.blit(img, (x, y))

def laad_levels(level):
    world_data = []
    with open (f'level{level}.txt', 'r') as file:
        for line in file:
            row = list(map(int, line.split()))
            world_data.append(row)
    return world_data

def reset_level(level):
    player.reset(32, 704 - 128)
    blob_group.empty()
    lava_group.empty()
    door_group.empty()
    door_fake_group.empty()
    world = World(laad_levels(level))
    return world

class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        action = False

        #muis positie
        positie = pygame.mouse.get_pos()

        #check muis geklikt op knop
        if self.rect.collidepoint(positie):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        #knop op scherm laden
        screen.blit(self.image, self.rect)

        return action

class Player():
    def __init__(self, x, y):
        self.reset(x, y)

    def update(self, game_over):
        dx = 0
        dy = 0
        walk_cooldown = 5
        col_thresh = 20

        if game_over == 0:
            key = pygame.key.get_pressed()
            if key[pygame.K_UP] and self.jumped == False and self.in_air == False:
                jump_fx.play()
                self.vel_y = -15
                self.jumped = True
            if key[pygame.K_UP] == False:
                self.jumped = False
            if key[pygame.K_LEFT]:
                dx -= 5
                self.counter += 1
                self.direction = -1
            if key[pygame.K_RIGHT]:
                dx += 5
                self.counter += 1
                self.direction = 1
            if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
                self.counter = 0
                self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]

            #animatie
            if self.counter >= walk_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]

            #zorgt dat speler tussen horizontale grenzen blijft
            if self.rect.x + dx < 0:
                dx = -self.rect.x
            if self.rect.x + dx + self.width > screen.get_width():
                dx = screen.get_width() - self.rect.x - self.width

            #zwaartekracht toevoegen
            self.vel_y += 1
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y
            
            #zorgt dat speler tussen verticale grenzen blijft
            if self.rect.y + dy < 0:
                dy = -self.rect.y
            if self.rect.y + dy + self.height > screen.get_height():
                dy = screen.get_height() - self.rect.y - self.height

            #kijken voor botsing
            self.in_air = True
            for tile in world.tile_list:
                #kijken voor botsing horizontaal/x richting
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                #kijken voor botsing verticaal/y richting
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    #kijken voor botsing als speler springt
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    #kijken voor botsing als speler valt
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
                        self.in_air = False

            #kijken voor botsing met enemy
            if pygame.sprite.spritecollide(self, blob_group, False):
                game_over = -1
                dead_fx.play()

            #kijken voor botsing met lava
            if pygame.sprite.spritecollide(self, lava_group, False):
                game_over = -1
                dead_fx.play()

            #kijken voor botsing met fake door
            if pygame.sprite.spritecollide(self, door_fake_group, False):
                game_over = -1
                dead_fx.play()

            #kijken voor botsing met deur
            if pygame.sprite.spritecollide(self, door_group, False):
                game_over = 1

            #kijken voor botsing met horizontaal platform
            for platform_horizontaal in platform_horizontaal_group:
                #botsing in horzontale richting
                if platform_horizontaal.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                #botsing in verticale richting
                if platform_horizontaal.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    #kijken voor botsing met onderkant
                    if abs((self.rect.top + dy) - platform_horizontaal.rect.bottom) < col_thresh:
                        self.vel_y = 0
                        dy = platform_horizontaal.rect.bottom - self.rect.top
                    #kijken voor botsing met bovenkant
                    elif abs((self.rect.bottom + dy) - platform_horizontaal.rect.top) < col_thresh:
                        self.rect.bottom = platform_horizontaal.rect.top - 1
                        dy = 0
                        self.in_air = False
                    #beweeg zijwaarts mee
                    self.rect.x += platform_horizontaal.move_direction

            #kijken voor botsing met verticaal platform
            for platform_verticaal in platform_verticaal_group:
                #botsing in horzontale richting
                if platform_verticaal.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                #botsing in verticale richting
                if platform_verticaal.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    #kijken voor botsing met onderkant
                    if abs((self.rect.top + dy) - platform_verticaal.rect.bottom) < col_thresh:
                        self.vel_y = 0
                        dy = platform_verticaal.rect.bottom - self.rect.top
                    #kijken voor botsing met bovenkant
                    elif abs((self.rect.bottom + dy) - platform_verticaal.rect.top) < col_thresh:
                        self.rect.bottom = platform_verticaal.rect.top - 1
                        dy = 0
                        self.in_air = False

            #update coördinaten van de speler
            self.rect.x += dx
            self.rect.y += dy

        elif game_over == -1:
            self.image = self.dead_img
            draw_text('GAME OVER', font, white, 928 // 2 - 100, 704 // 2 - 100)

        #speler op scherm laden
        screen.blit(self.image, self.rect)

        return game_over

    def reset(self, x, y):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        for num in range(1, 5):
            img_right = pygame.image.load(f'meisje{num}.png')
            img_right = pygame.transform.scale(img_right, (32, 64))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.dead_img = pygame.image.load('dood.png')
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.direction = 0
        self.in_air = True

class World():
    def __init__(self, data):
        self.tile_list = []

        row_count = 0
        for row in data:
            column_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(grond_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = column_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    img = pygame.transform.scale(gras_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = column_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 3:
                    blob = Enemy(column_count * tile_size, row_count * tile_size)
                    blob_group.add(blob)
                    if level == 5:
                        blob = Enemy_boss(column_count * tile_size, row_count * tile_size)
                        blob_group.add(blob)
                if tile == 4:
                    lava = Lava(column_count * tile_size, row_count * tile_size + (tile_size // 2))
                    lava_group.add(lava)
                if tile == 5:
                    door = Door(column_count * tile_size, row_count * tile_size - (tile_size // 2))
                    door_group.add(door)
                if tile == 6:
                    coin = Coin(column_count * tile_size + (tile_size // 2), row_count * tile_size + (tile_size // 2))
                    coin_group.add(coin)
                if tile == 7:
                    platform_horizontaal = Platform_horizontaal(column_count * tile_size, row_count * tile_size)
                    platform_horizontaal_group.add(platform_horizontaal)
                if tile == 8:
                    platform_verticaal = Platform_verticaal(column_count * tile_size, row_count * tile_size)
                    platform_verticaal_group.add(platform_verticaal)
                if tile == 9:
                    door_fake = Door_fake(column_count * tile_size, row_count * tile_size + (tile_size // 2))
                    door_fake_group.add(door_fake)
                column_count += 1
            row_count += 1
    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        blob_img = pygame.image.load("blob.png")
        self.image = pygame.transform.scale(blob_img, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0
    
    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1

class Enemy_boss(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        blob_img = pygame.image.load("blob_boss.png")
        self.image = pygame.transform.scale(blob_img, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0
    
    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1

class Lava(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        lava_img = pygame.image.load("lava.png")
        self.image = pygame.transform.scale(lava_img, (tile_size, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        coin_img = pygame.image.load("coin.png")
        self.image = pygame.transform.scale(coin_img, (tile_size // 2, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

class Door(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        door_img = pygame.image.load("door.png")
        self.image = pygame.transform.scale(door_img, (tile_size, int(tile_size * 1.5)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Platform_horizontaal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        platform_img = pygame.image.load("gras.png")
        self.image = pygame.transform.scale(platform_img, (tile_size, (tile_size // 2)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_counter = 0
        self.move_direction = 1

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1

class Platform_verticaal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        platform_img = pygame.image.load("gras.png")
        self.image = pygame.transform.scale(platform_img, (tile_size, (tile_size // 2)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_counter = 0
        self.move_direction = 1

    def update(self):
        self.rect.y += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1

class Door_fake(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        door_fake_img = pygame.image.load("door.png")
        self.image = pygame.transform.scale(door_fake_img, (tile_size, int(tile_size * 1.5)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

player = Player(32, 704 - 128)

blob_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
door_group = pygame.sprite.Group()
platform_horizontaal_group = pygame.sprite.Group()
platform_verticaal_group = pygame.sprite.Group()
door_fake_group = pygame.sprite.Group()

world = World(laad_levels(level))

#buttons
restart_button = Button(928 // 2 - 130, 704 // 2, restart_img)
play_button = Button(928 // 2 - 350, 704 // 2 + 100, play_img)
stop_button = Button(928 // 2 + 100, 704 // 2 + 100, stop_img)

#muntje voor bovenaan het scherm
score_coin = Coin((tile_size // 2), (tile_size // 2))
coin_group.add(score_coin)
high_score_coin = Coin((tile_size * 28), (tile_size //2))
coin_group.add(high_score_coin)


run = True
while run:
    clock.tick(fps)
    screen.blit(achtergrond_img, (0, 0))

    if level == 5:
        achtergrond_img = achtergrond_boss_img

    if main_menu == True:
        if play_button.draw():
            main_menu = False
        if stop_button.draw():
            run = False
    else:
        world.draw()

        if game_over == 0:
            blob_group.update()
            platform_horizontaal_group.update()
            platform_verticaal_group.update()
            #score updaten
            #check of er muntjes zijn verzameld
            if pygame.sprite.spritecollide(player, coin_group, True):
                score += 1
                coin_fx.play()
            draw_text('X' + str(score), font_score, white, tile_size - 10, 10)
    
        blob_group.draw(screen)
        lava_group.draw(screen)
        coin_group.draw(screen)
        door_group.draw(screen)
        platform_horizontaal_group.draw(screen)
        platform_verticaal_group.draw(screen)
        door_fake_group.draw(screen)

        game_over = player.update(game_over)

        #als speler dood is
        if game_over == -1:
            if restart_button.draw():
                world_data = []
                platform_horizontaal_group.empty()
                platform_verticaal_group.empty()
                world = reset_level(level)
                game_over = 0
                score = 0

        #als speler level voltooid heeft
        if game_over == 1:
            level += 1
            if level <= max_levels:
                world_data = []
                platform_horizontaal_group.empty()
                platform_verticaal_group.empty()
                coin_group.empty()
                coin_group.add(score_coin)
                coin_group.add(high_score_coin)
                world = reset_level(level)
                game_over = 0
            else:
                victory_fx.play()
                draw_text('JE HEBT GEWONNEN!', font, white, 928 // 2 - 160, 704 // 2 - 100)
                if restart_button.draw():
                    level = 1
                    world_data = []
                    world = reset_level(level)
                    game_over = 0
                    score = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    pygame.display.update()
pygame.quit()