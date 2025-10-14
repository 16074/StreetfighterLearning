import pygame
import sys
import os
pygame.init()

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller .exe"""
    try:
        base_path = sys._MEIPASS  # temp folder for .exe
    except Exception:
        base_path = os.path.abspath(".")  # current folder for .py

    return os.path.join(base_path, relative_path)

# Window voor scherm
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

info = pygame.display.Info()
screen_width, screen_height = info.current_w, info.current_h

Screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("WiSp --- Home")

# Achtergrond inladen
bg_image = pygame.image.load(resource_path("afbeeldingen/achtergrond/math.png")).convert_alpha()
bg_image = pygame.transform.scale(bg_image, (screen_width, screen_height))

def draw_bg():
    Screen.blit(bg_image, (0, 0))

# Kleuren en fonts
BUTTON_COLOR = (255, 253, 186)
BUTTON_HOVER_COLOR = (255, 251, 117)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

font = pygame.font.Font(None, 34)
font2 = pygame.font.Font(None, 46)

# Button klasse
class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.Font(None, 26)
        self.color = BUTTON_COLOR
        self.hover_color = BUTTON_HOVER_COLOR

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(surface, self.hover_color, self.rect)
        else:
            pygame.draw.rect(surface, self.color, self.rect)

        text_surface = self.font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos)

# Maak knoppen één keer aan
button1 = Button(((screen_width-400)/2), 210, 400, 75, "Streetfighter - Pythagoras")
button2 = Button(((screen_width-400)/2), 310, 400, 75, "Sollies klaslokaal - Machtrekenen")
button3 = Button(((screen_width-400)/2), 410, 400, 75, "Platformer - SosCasToa")

current_screen = "home"

# Hoofdloop
run = True
while run:
    # Event handler (alleen hier!)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Check klikken
        if current_screen == "home":
            if button1.is_clicked(event):
                current_screen = 'game1'
            if button2.is_clicked(event):
                current_screen = 'game2'
            if button3.is_clicked(event):
                current_screen = 'game3'
        
    if current_screen == "home":
        draw_bg()

        titeltekst = font2.render("Welkom in WiSp!", True, WHITE)
        vraagtekst = font.render("Selecteer hieronder een level om wiskunde mee te oefenen:", True, WHITE)
        Screen.blit(titeltekst, ((screen_width - titeltekst.get_width()) / 2, 80))
        Screen.blit(vraagtekst, ((screen_width - vraagtekst.get_width()) / 2, 120))

        button1.draw(Screen)
        button2.draw(Screen)
        button3.draw(Screen)

    elif current_screen == "game1":
        with open("start.py", "r") as f:
            code = f.read()
        exec(code)

    elif current_screen == "game2":
        with open("sprite.py", "r") as f:
            code = f.read()
        exec(code)

    elif current_screen == "game3":
        with open("game.py", "r") as f:
            code = f.read()
            exec(code)        

    else:
        # Simpel wit scherm als placeholder voor spel
        Screen.fill(WHITE)
        speltekst = font.render(f"Je bent nu in {current_screen}", True, BLACK)
        Screen.blit(speltekst, (SCREEN_WIDTH/2 - speltekst.get_width()/2, SCREEN_HEIGHT/2))

    # Update display
    pygame.display.update()

# Einde van programma
pygame.quit()
