import pygame
pygame.init()

# Window voor scherm
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
Screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Fighter")

# Achtergrond inladen
bg_image = pygame.image.load("afbeeldingen/achtergrond/math.png").convert_alpha()
bg_image = pygame.transform.scale(bg_image, (1000, 600))

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

    def is_clicked(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
            return True
        return False

# Maak knoppen één keer aan
button1 = Button(100, 210, 400, 75, "Streetfighter - Pythagoras")
button2 = Button(100, 310, 400, 75, "NKPgame - Machtrekenen")
button3 = Button(100, 410, 400, 75, "Platformer - SosCasToa")

# Hoofdloop
run = True
while run:
    draw_bg()

    # Titel en instructie
    titeltekst = font2.render("Welkom in Wisp!", True, WHITE)
    vraagtekst = font.render("Selecteer hieronder een level om wiskunde mee te oefenen:", True, WHITE)
    Screen.blit(titeltekst, ((SCREEN_WIDTH - titeltekst.get_width()) / 2, 80))
    Screen.blit(vraagtekst, ((SCREEN_WIDTH - vraagtekst.get_width()) / 2, 120))

    # Teken knoppen
    button1.draw(Screen)
    button2.draw(Screen)
    button3.draw(Screen)

    # Event handler (alleen hier!)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Check klikken
    if button1.is_clicked():
        Screen.fill(WHITE)
    if button2.is_clicked():
        Screen.fill(WHITE)
    if button3.is_clicked():
        Screen.fill(WHITE)

    # Update display
    pygame.display.update()

# Einde van programma
pygame.quit()
