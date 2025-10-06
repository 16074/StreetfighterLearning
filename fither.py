import pygame
import os

class Fighter():
    def __init__(self, x, y):
        # Frames van je GIF (png's)
        self.frames = []
        self.load_images("afbeeldingen/Ken")  # map met png frames
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.animation_speed = 1  # hoe snel frames wisselen

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

    def draw(self, surface):
        surface.blit(self.image, self.rect)
