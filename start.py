import pygame
import os
import sys
from fither import Fighter
from fither import Kak
from fither import Health
from fither import Button
from fither import Vraag
from fither import UitlegVenster


pygame.init()

#tijd
damage_timer = None
Damage_result = None
animating = False
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

#yo
vraag_window = Vraag(300, 150, 400, 250)

#vraagknop
vraag_knop = Button(450, 250, 120, 40, "Vraag")

#lkj
uitleg_knop = Button(900, 0, 100, 40, "Uitleg")

#uitleg window
uitleg_window = UitlegVenster(200, 100, 600, 400)

#f
attack_start = None
damage_applied = False

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

    #vraagknop draw
    vraag_knop.draw(Screen)

    #vraag op scherm
    vraag_window.draw(Screen)

    #uitleg knop op scherm
    uitleg_knop.draw(Screen)

    #uitleg op scherm
    uitleg_window.draw(Screen)

#event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False 

        vraag_window.handle_event(event)

    if vraag_knop.is_clicked(event):
        vraag_window.active = True  # opent de vraag
    vraag_window.handle_event(event)
    uitleg_window.handle_event(event)

    if uitleg_knop.is_clicked(event):
        uitleg_window.active = True
    
    
    if button1.is_clicked(event):
        pygame.quit() 
        os.system("python main.py")
        sys.exit()

    if vraag_window.correct is not None and damage_timer is None:
        damage_timer = pygame.time.get_ticks()
        Damage_result= vraag_window.correct
    
    if damage_timer is not None and not animating:
        if pygame.time.get_ticks() - damage_timer >= 2000:
            animating = True

            if Damage_result:
                fighter_1.play("attack")
                attack_start = pygame.time.get_ticks()
                #fighter_2.play("hurt")
            else:
                fighter_2.play("attack")
                attack_start = pygame.time.get_ticks()
                #fighter_1.play("hurt")

    if animating and attack_start is not None:
        elapsed = pygame.time.get_ticks() - attack_start

        # start hurt na 0.5 seconde
        if elapsed >= 500 and not damage_applied:  
            if Damage_result:
                fighter_2.play("hurt")
                fighter_2.health -= 10
            else:   
                fighter_1.play("hurt")
                fighter_1.health -= 10
            damage_applied = True

        elif elapsed >= 1500:
            vraag_window.correct = None
            vraag_window = Vraag(300, 150, 400, 250)
            damage_timer = None
            Damage_result = None
            animating = False
            attack_start = None
            damage_applied = False

        
#update display
    pygame.display.update()

#sluiten

pygame.quit()