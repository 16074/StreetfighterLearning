#screen settings
import pygame
pygame.init()

info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h

Screen = pygame.display.set_mode((WIDTH, HEIGHT))

FPS = 60

#button settings
WHITE = (255, 255, 255)
BUTTON_HOVER_COLOR = (99, 172, 187)
BUTTON_COLOR = (71, 191, 208)
LIGHT_YELLOW = (255, 255, 185)

#player settings
X_PLAYER_START = WIDTH/4
Y_PLAYER_START = HEIGHT/4
SPEED_PLAYER = 1
PLAYER_SIZE = 1.5
SPELERRADIUS = 150
ANIMATIONSPEED = 0.05

#Tafelsetting
TAFELSIZE = 2.75

#shootsettings
SHOOT_COOLDOWN = 15    
BULLET_SCALE = 1.4
BULLET_SPEED = 10

#producbar
PRODUCBARBREEDTE = 90
PRODUCBARHOOGTE = 40

#vraagbox setting
QUESTIONSIZE = 0.08

#setting
SETTINGGROOTE = 0.2

#animatiesetting
ANIMATIONCOOLDOWN = 100