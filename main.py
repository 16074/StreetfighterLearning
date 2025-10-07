import pygame
pygame.init()

#window voor scherm
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
Screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Fighter")

#inladen achtergrond
bg_image = pygame.image.load("afbeeldingen/achtergrond/math.png").convert_alpha()
bg_image = pygame.transform.scale(bg_image,(1000 , 600))

#achtergrond afspelen
def draw_bg():
    Screen.blit(bg_image, (0,0))

#loop
run = True
while run: 
    
    #achtergrond tekenen
    draw_bg()

    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False 
    #update display
    pygame.display.update()

pygame.quit()