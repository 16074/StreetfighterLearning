import pygame
from fither import Fighter
from fither import Kak
from fither import Health
from fither import Button


pygame.init()

#window voor scherm
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
Screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Level 1 --- Streetfighter/Pythagoras")

#inladen achtergrond
bg_image = pygame.image.load("afbeeldingen/achtergrond/Achtergrond.jpg").convert_alpha()
bg_image = pygame.transform.scale(bg_image,(1000 , 600))

#achtergrond afspelen
def draw_bg():
    Screen.blit(bg_image, (0,0))

#enkele fighter
fighter_1 = Fighter(-25,100,)
fighter_2 = Kak(425,100,)

#asdf;lj
health_bar_1= Health(175,250)
health_bar_2= Health(625,250)

#Button
button1 = Button(0, 0, 100, 40, "Terug")


#loop

run = True
while run: 
    
    #achtergrond tekenen
    draw_bg()

    #button
    button1.draw(Screen)

    #fighter op scherm
    fighter_1.draw(Screen)
    fighter_2.draw(Screen)

    # update fighters
    fighter_1.update()
    fighter_2.update()

    #healthbar op scherm
    health_bar_1.draw(Screen, fighter_1.health, fighter_1.max_health)
    health_bar_2.draw(Screen, fighter_2.health, fighter_2.max_health)

#event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if button1.is_clicked(event):
            with open("main.py", "r") as f:
                code = f.read()
            exec(code)
#update display
    pygame.display.update()

#sluiten

pygame.quit()
    


