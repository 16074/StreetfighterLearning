import pygame
import os
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
    


