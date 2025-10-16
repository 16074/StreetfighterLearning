import pygame
import os
import random
from Vragen import PYTHAGORAS_VRAGEN  

# Kleuren en fonts
BUTTON_COLOR = (128, 0, 128)
BUTTON_HOVER_COLOR = (108, 70, 117)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Fighter():
    def __init__(self, x, y):
        # Frames van je GIF (png's)
        self.frames = []
        self.load_images("afbeeldingen/idle")  # map met png frames
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.animation_speed = 0.3  # hoe snel frames wisselen
        self.max_health = 100
        self.health = self.max_health

        #frames tonen
    
    def draw(self, surface):
        image = pygame.transform.rotozoom(self.image.convert_alpha(), 1, 2.3) 
        # schaal bijvoorbeeld 2x groter 
        surface.blit(image, self.rect)

        scaled_image = pygame.transform.scale(self.image, (150, 150))

    def load_images(self, folder_path):
        for filename in sorted(os.listdir(folder_path)):
            if filename.endswith(".png"):
                img = pygame.image.load(os.path.join(folder_path, filename)).convert_alpha()
                self.frames.append(img)

    def update(self):
        # animatie updaten
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    #def draw(self, surface):
        #surface.blit(self.image, self.rect)
        

class Kak():
    def __init__(self, x, y):
        # Frames van je GIF (png's)
        self.frames = []
        self.load_images("afbeeldingen/idle")  # map met png frames
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.animation_speed = 0.3  # hoe snel frames wisselen
        self.max_health = 100
        self.health = self.max_health

        #frames tonen
    
    def draw(self, surface):
        image = pygame.transform.rotozoom(self.image.convert_alpha(), 180, 2.3) 
        image= pygame.transform.flip(image,flip_x= False, flip_y=True)
        # schaal bijvoorbeeld 2x groter 
        surface.blit(image, self.rect)

        scaled_image = pygame.transform.scale(self.image, (150, 150))

    def load_images(self, folder_path):
        for filename in sorted(os.listdir(folder_path)):
            if filename.endswith(".png"):
                img = pygame.image.load(os.path.join(folder_path, filename)).convert_alpha()
                self.frames.append(img)

    def update(self):
        # animatie updaten
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

class Health:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, surface, health, max_health):
        ratio = health / max_health
        # rode achtergrond
        pygame.draw.rect(surface, (255, 0, 0), (self.x, self.y, 200, 20))
        # groene foreground
        pygame.draw.rect(surface, (0, 255, 0), (self.x, self.y, 200 * ratio, 20))
        
class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.Font(None, 20)
        self.color = BUTTON_COLOR
        self.hover_color = BUTTON_HOVER_COLOR

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(surface, self.hover_color, self.rect)
        else:
            pygame.draw.rect(surface, self.color, self.rect)

        text_surface = self.font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos)
    
class Vraag:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = pygame.font.Font(None, 20)
        self.small_font = pygame.font.Font(None, 28)
        self.active = False        
        self.user_text = ""        
        self.correct = None        

        #
        self.vraag_data = random.choice(PYTHAGORAS_VRAGEN)
        self.vraag_tekst = self.vraag_data["vraag"]
        self.answer = self.vraag_data["antwoord"]

        # knop om te bevestigen
        self.button_rect = pygame.Rect(
            x + width // 2 - 50, 
            y + height - 60, 
            100, 
            40
        )

    def draw(self, surface):
        """Teken het venster op het scherm"""
        if not self.active:
            return

        # achtergrond venster
        pygame.draw.rect(surface, (200, 200, 255), self.rect)
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 3)

        # vraagtekst
        vraag_text = self.font.render(self.vraag_tekst, True, (0, 0, 0))
        surface.blit(vraag_text, (self.rect.x + 20, self.rect.y + 20))

        # invoerveld
        input_rect = pygame.Rect(self.rect.x + 30, self.rect.y + 80, 140, 40)
        pygame.draw.rect(surface, (255, 255, 255), input_rect)
        pygame.draw.rect(surface, (0, 0, 0), input_rect, 2)

        # getypte tekst
        input_surface = self.small_font.render(self.user_text, True, (0, 0, 0))
        surface.blit(input_surface, (input_rect.x + 10, input_rect.y + 8))

        # bevestig-knop
        pygame.draw.rect(surface, (150, 150, 255), self.button_rect)
        btn_text = self.small_font.render("Bevestig", True, (0, 0, 0))
        surface.blit(
            btn_text,
            (
                self.button_rect.centerx - btn_text.get_width() // 2,
                self.button_rect.centery - btn_text.get_height() // 2
            )
        )

        # feedback bij goed/fout antwoord
        if self.correct is True:
            result_text = self.small_font.render("✅ Goed zo!", True, (0, 200, 0))
            surface.blit(result_text, (self.rect.x + 30, self.rect.y + 140))
        elif self.correct is False:
            result_text = self.small_font.render("❌ Fout! Probeer opnieuw.", True, (200, 0, 0))
            surface.blit(result_text, (self.rect.x + 30, self.rect.y + 140))

    def handle_event(self, event):
        """Verwerk toetsen en muisklikken"""
        if not self.active:
            return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.check_answer()
            elif event.key == pygame.K_BACKSPACE:
                self.user_text = self.user_text[:-1]
            elif event.unicode.isnumeric():
                self.user_text += event.unicode

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.button_rect.collidepoint(event.pos):
                self.check_answer()

    def check_answer(self):
        """Controleer het antwoord"""
        try:
            if int(self.user_text) == self.answer:
                self.correct = True
            else:
                self.correct = False
        except ValueError:
            self.correct = False
        if not self.active:
            return
