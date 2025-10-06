import pygame
from fither import Fighter
pygame.init()

#window voor scherm
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
Screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Fighter")

#inladen achtergrond
bg_image = pygame.image.load("afbeeldingen/achtergrond/Achtergrond.jpg").convert_alpha()
bg_image = pygame.transform.scale(bg_image,(1000 , 600))

#achtergrond afspelen
def draw_bg():
    Screen.blit(bg_image, (0,0))

#enkele fighter
fighter_1 = Fighter(200,310)
fighter_2 = Fighter(700,310)

#loop
run = True
while run: 
    
    #achtergrond tekenen
    draw_bg()


    #fighter op scherm
    fighter_1.draw(Screen)
    fighter_2.draw(Screen)

    # update fighters
    fighter_1.update()
    fighter_2.update()

#event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False 
#update display
    pygame.display.update()

#sluiten

pygame.quit()
    


