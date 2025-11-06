from settings import *
counter1 = 0
laatste_vuur_spawn = 0 
import json
from tkinter import messagebox
import random
import math
import sys
import subprocess

import pygame
info = pygame.display.Info()
screen_width, screen_height = 1000, 600

#Screen = pygame.display.set_mode((1000, 600))
#pygame.display.set_caption("WiSp --- Home")

def check_library_installed(libraryname):
    try:
        __import__(libraryname)
    except ImportError:
        print(f"Installing necessary packages {str(libraryname)}")
        subprocess.check_call([sys.executable, "-m", "pip", "install", libraryname])

libraries = ["pygame", "pygame-ce", "opencv-python"]
for i in libraries:
    check_library_installed(i)
import pygame
import cv2
pygame.init()
playerscore = 0

#vragenmodus staat aan of uit
questionoo = False

#create window
pygame.font.init()

video_path = "NKPGAME/DIEFILMPJE1.mp4"
video_path2 = "NKPGAME/DIEFILMPJE2.mp4"
video = cv2.VideoCapture(video_path)
video2 = cv2.VideoCapture(video_path2)
videofps = video.get((cv2.CAP_PROP_FPS))/3
pygame.mixer.init()
pygame.mixer.music.load("NKPGAME/NKPGAMESOUND.mp3")
pygame.mixer.music.play(loops=-1, start=0, fade_ms=1000)
pygame.mixer.music.set_volume(0.45)
score_font = pygame.font.Font('freesansbold.ttf', 16)
GROOT_font = pygame.font.Font('freesansbold.ttf', 32)
GROOOOT_font = pygame.font.Font('NKPGAME/bloody.TTF', 90)
blbl = score_font.render("B", False, (0,0,0)) # initialiseer om te kijken hoe groot het lettertype op scherm is
score_height = blbl.get_height()
SCREENHEIGHT = score_height + HEIGHT
page = pygame.display.set_mode((WIDTH, SCREENHEIGHT))
screen = pygame.Surface((WIDTH, HEIGHT))
pygame.display.set_caption("Level 2 --- Sollies klaslokaal / Machtrekenen")
clock = pygame.time.Clock()
objects = []
objects_rect = []
tafel_links = pygame.transform.rotozoom(pygame.image.load("NKPGAME/Tafelart.png"), 270, TAFELSIZE)
HEIGHT_tafel = tafel_links.get_height()
WIDTH_tafel = tafel_links.get_width()
for i in range(math.floor(HEIGHT / HEIGHT_tafel)):
    Y = i * HEIGHT_tafel
    rect = pygame.Rect(-20, Y, WIDTH_tafel, HEIGHT_tafel)
    objects.append((tafel_links, rect))
for i in range(math.floor(HEIGHT / HEIGHT_tafel) - 1):
    Y = i * HEIGHT_tafel
    rect = pygame.Rect((WIDTH / 2) - 20, Y, WIDTH_tafel, HEIGHT_tafel)
    objects.append((tafel_links, rect))
tafel_rechts = pygame.transform.rotozoom(pygame.image.load("NKPGAME/Tafelart.png"), 90, TAFELSIZE)
for i in range(math.floor(HEIGHT / HEIGHT_tafel)):
    Y = i * HEIGHT_tafel
    rect = pygame.Rect(WIDTH - WIDTH_tafel + 20, Y, WIDTH_tafel, HEIGHT_tafel)
    objects.append((tafel_rechts, rect))
for i in range(math.floor(HEIGHT / HEIGHT_tafel) - 1):
    Y = i * HEIGHT_tafel
    rect = pygame.Rect(WIDTH - (WIDTH / 2) - WIDTH_tafel + 20, Y, WIDTH_tafel, HEIGHT_tafel)
    objects.append((tafel_rechts, rect))

#score inladen
a = open("highscore.txt", "r")
x = a.read()
a.close()
if x == "":
    x = 0
highscore = int(x)

def display_score(score_font):
    box_text =  score_font.render(f"Aantal vragen: {str(len(vraagbox_lijst))}   score: {str(playerscore)}  highscore: {str(highscore)}", True, (0,0,0))
    text_surface = pygame.Surface((WIDTH, box_text.get_height() + 30))
    text_surface.fill((180, 210, 186))
    text_surface.blit(box_text, ((WIDTH - box_text.get_width())/2, 0))
    page.blit(text_surface, (0, 0))

#sprites inladen
background = pygame.image.load("NKPGAME/BACKGROUNDTILE.png")
y_background = background.get_height()
x_background = background.get_width()

#begin vragendeel
def questiontime():
    vraag = []
    antwoordenlijst = []
    goedantwoord = []
    font = pygame.font.Font(None, 22)
    font2 = pygame.font.Font(None, 34)

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

            #Laad text
            text_surface = self.font.render(self.text, True, WHITE)
            text_rect = text_surface.get_rect(center=self.rect.center)
            surface.blit(text_surface, text_rect)

        def is_clicked(self):
            mouse_pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
                return True
            else:
                return False
    
    #ophalen quizvragen uit json file
    with open('data.json', 'r') as file:
        data = json.load(file)

    def load_random_question():
        vraag_data = random.choice(data["vragen"])
        vraag_functie = vraag_data["vraag"]
        vraag.append(vraag_functie)

        goed_antwoord = vraag_data["goed_antwoord"]
        goedantwoord.append(goed_antwoord)
        fout_antwoorden = [vraag_data["fout_antwoord1"], vraag_data["fout_antwoord2"]]

        antwoorden = [goed_antwoord] + fout_antwoorden
        antwoordenlijst.extend(antwoorden)
        antwoordenlijst.sort()

    def check_answer(selected_answer, correct_answer):
        if selected_answer == correct_answer:
            messagebox.showinfo("Resultaat vraag", "Heel goed! Je hebt weer een leerling geholpen!")
            return "Vraag goed"
        else:
            messagebox.showerror("Resultaat vraag", "Helaas! Probeer een andere vraag te beantwoorden.\nHet goede antwoord was " + correct_answer)
            screen.fill(LIGHT_YELLOW)
            vraag.clear()
            antwoordenlijst.clear()
            goedantwoord.clear()
            load_random_question()
            titletekst = font2.render("Beantwoord een vraag vanuit de klas:", True, (0,0,0))
            vraagtekst = font.render(vraag[0], True, (0,0,0))
            screen.blit(titletekst, ((WIDTH - titletekst.get_width())/2,80))
            screen.blit(vraagtekst, ((WIDTH - vraagtekst.get_width())/2,120))
            button1 = Button(100, 210, 400, 75, antwoordenlijst[0])
            button2 = Button(100, 310, 400, 75, antwoordenlijst[1])
            button3 = Button(100, 410, 400, 75, antwoordenlijst[2])
            button1.draw(screen)
            button2.draw(screen)
            button3.draw(screen)
        
    load_random_question()
    screen.fill(LIGHT_YELLOW)
    titeltekst = font2.render("Beantwoord een vraag vanuit de klas:", True, (0,0,0))
    vraagtekst = font.render(vraag[0], True, (0,0,0))
    screen.blit(titeltekst, ((WIDTH - titeltekst.get_width())/2,80))
    screen.blit(vraagtekst, ((WIDTH - vraagtekst.get_width())/2,120))

    def button_loop():
        button1.draw(screen)
        button2.draw(screen)
        button3.draw(screen)

    running = True
    while running:
        button1 = Button(((screen_width-400)/2), 210, 400, 75, antwoordenlijst[0])
        button2 = Button(((screen_width-400)/2), 310, 400, 75, antwoordenlijst[1])
        button3 = Button(((screen_width-400)/2), 410, 400, 75, antwoordenlijst[2])
        button_loop()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return "SPEL STOPT"
        if button1.is_clicked():
            if check_answer(str(antwoordenlijst[0]), str(goedantwoord[0])):
                return "Vraag goed"
        if button2.is_clicked():
            if check_answer(str(antwoordenlijst[1]), str(goedantwoord[0])):
                return "Vraag goed"
        if button3.is_clicked():
            if check_answer(str(antwoordenlijst[2]), str(goedantwoord[0])):
                return "Vraag goed"

        #Update display
        page.blit(screen, (0, SCREENHEIGHT - HEIGHT))
        pygame.display.flip()

#begin subsectie vraagtekens
vraagbox_img = pygame.transform.rotozoom(pygame.image.load("NKPGAME/QUESTION.png"), 0, QUESTIONSIZE)
vraagbox_hoogte = vraagbox_img.get_height()
vraagbox_breedte = vraagbox_img.get_width()
vraagbox_lijst = []
def check_valid(vraagbox_rect):
    for _, obj_rect in objects:
        if vraagbox_rect.colliderect(obj_rect):
            return False
    for ques_rect in vraagbox_lijst:
        if vraagbox_rect.colliderect(ques_rect):
            return False
    try:
        if vraagbox_lijst.colliderect(player.player_rect):
            return False
    except:
        return True
    return True

def add_questionbox():
    while True:
        x_cord = random.randint(0, WIDTH-vraagbox_breedte)
        y_cord = random.randint(0, HEIGHT-vraagbox_hoogte)
        vraagbox_rect = pygame.Rect(x_cord, y_cord, vraagbox_breedte, vraagbox_hoogte)

        # Controleer of de positie geldig is
        if check_valid(vraagbox_rect):
            vraagbox_lijst.append(vraagbox_rect)
            break  # Stop de lus zodra een geldige positie is gevonden

#einde subsectie + vragendeel

#player info en animatie
image = pygame.transform.rotozoom(pygame.image.load("NKPGAME/NKPstanding1.0.png").convert_alpha(), 0, PLAYER_SIZE)
frame2 = pygame.transform.rotozoom(pygame.image.load("NKPGAME/frame2.png").convert_alpha(), 0, PLAYER_SIZE)
frame3 = pygame.transform.rotozoom(pygame.image.load("NKPGAME/frame3.png").convert_alpha(), 0, PLAYER_SIZE)
frame4 = pygame.transform.rotozoom(pygame.image.load("NKPGAME/frame4.png").convert_alpha(), 0, PLAYER_SIZE)
frame5 = pygame.transform.rotozoom(pygame.image.load("NKPGAME/frame5.png").convert_alpha(), 0, PLAYER_SIZE)
frame6 = pygame.transform.rotozoom(pygame.image.load("NKPGAME/frame6.png").convert_alpha(), 0, PLAYER_SIZE)
frame7 = pygame.transform.rotozoom(pygame.image.load("NKPGAME/frame7.png").convert_alpha(), 0, PLAYER_SIZE)
kimage = pygame.transform.rotozoom(pygame.image.load("NKPGAME/KASTELEINstanding1.0.png").convert_alpha(), 0, PLAYER_SIZE/2)
KASframe2 = pygame.transform.rotozoom(pygame.image.load("NKPGAME/KASframe2.png").convert_alpha(), 0, PLAYER_SIZE/1.5)
KASframe3 = pygame.transform.rotozoom(pygame.image.load("NKPGAME/KASframe3.png").convert_alpha(), 0, PLAYER_SIZE/1.5)
KASframe4 = pygame.transform.rotozoom(pygame.image.load("NKPGAME/KASframe4.png").convert_alpha(), 0, PLAYER_SIZE/1.5)
KASframe5 = pygame.transform.rotozoom(pygame.image.load("NKPGAME/KASframe5.png").convert_alpha(), 0, PLAYER_SIZE/1.5)
KASframe6 = pygame.transform.rotozoom(pygame.image.load("NKPGAME/KASframe6.png").convert_alpha(), 0, PLAYER_SIZE/1.5)
KASframe7 = pygame.transform.rotozoom(pygame.image.load("NKPGAME/KASframe7.png").convert_alpha(), 0, PLAYER_SIZE/1.5)
frame = 0
framelijst = [image, frame2, frame3, frame4, frame5, frame6, frame7]
kframelijst = [kimage, KASframe2, KASframe3, KASframe4, KASframe5, KASframe6, KASframe7]
last_update = pygame.time.get_ticks()
PLAYER_WIDTH = image.get_width()
PLAYER_HEIGHT = image.get_height()
i_y = math.ceil(HEIGHT/y_background)
i_x = math.ceil(WIDTH/x_background)
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__
        self.angle = 270
        self.image = image
        self.PLAYER_WIDTH = PLAYER_WIDTH
        self.PLAYER_HEIGHT = PLAYER_HEIGHT
        self.pos = pygame.math.Vector2(X_PLAYER_START, Y_PLAYER_START)
        self.base_player_img = self.image
        self.shoot =  False
        self.shoot_cooldown = 0
        self.last_update = last_update
        self.frame = 0
        self.secret_unlocked = False

    def player_animation(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update >= ANIMATIONCOOLDOWN:
            self.last_update = current_time
            self.frame += 1
            if self.frame >= len(framelijst):  # Reset naar begin van animatie
                self.frame = 1
        elif self.snelheid_x == 0 and self.snelheid_y == 0:
            print("", end="")
            #return 0

    def user_input(self):
        self.snelheid_x = 0
        self.snelheid_y = 0
        self.player_animation()
        if self.secret_unlocked:
            character = kframelijst[self.frame].copy()
        else:
            character = framelijst[self.frame]
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.snelheid_y = -SPEED_PLAYER
            self.image = pygame.transform.rotate(character, 180)
            self.angle = 90
        if keys[pygame.K_s]:
            self.snelheid_y = SPEED_PLAYER
            self.image = pygame.transform.rotate(character, 0)
            self.angle = 270
        if keys[pygame.K_a]:
            self.snelheid_x = -SPEED_PLAYER
            self.image = pygame.transform.rotate(character, 270)
            self.angle = 180
        if keys[pygame.K_d]:
            self.snelheid_x = SPEED_PLAYER
            self.image = pygame.transform.rotate(character, 90)
            self.angle = 0
        if keys[pygame.K_w] and keys[pygame.K_d]:
            self.image = pygame.transform.rotate(character, 135)
            self.angle = 45
        elif keys[pygame.K_w] and keys[pygame.K_a]:
            self.image = pygame.transform.rotate(character, 225)
            self.angle = 135
        elif keys[pygame.K_s] and keys[pygame.K_d]:
            self.image = pygame.transform.rotate(character, 45)
            self.angle = 315
        elif keys[pygame.K_s] and keys[pygame.K_a]:
            self.image = pygame.transform.rotate(character, 315)
            self.angle = 225 
        if self.snelheid_x != 0 and self.snelheid_y !=0:
            self.snelheid_x = self.snelheid_x/math.sqrt(2)
            self.snelheid_y = self.snelheid_y/math.sqrt(2)
        if pygame.mouse.get_pressed() == (1,0,0,) or keys[pygame.K_SPACE]:
            self.shoot = True
            self.is_shooting()
        else: 
            self.shoot = False

    def is_shooting(self):
        if self.shoot_cooldown == 0:
            self.shoot_cooldown = SHOOT_COOLDOWN
            spawn_bullet_pos = (self.pos.x + self.PLAYER_WIDTH // 2,
                                self.pos.y + self.PLAYER_HEIGHT // 2)
            self.bullet = bullet(spawn_bullet_pos[0], spawn_bullet_pos[1], self.angle)
            bullet_group.add(self.bullet)

    def wall_collisions(self):
        if self.pos.x < 0:
            self.pos.x = 0
            self.snelheid_x = 0
        if self.pos.x + self.PLAYER_WIDTH > WIDTH:
            self.pos.x = WIDTH - self.PLAYER_WIDTH
            self.snelheid_x = 0
        if self.pos.y < 0:
            self.pos.y = 0
            self.snelheid_y = 0
        if self.pos.y + self.PLAYER_HEIGHT > HEIGHT:
            self.pos.y = HEIGHT - self.PLAYER_HEIGHT
            self.snelheid_y = 0

    def object_collision(self):
        player_rect = pygame.Rect(self.pos.x, self.pos.y, self.PLAYER_WIDTH, self.PLAYER_HEIGHT)

        # Controleer botsing op de x-as
        self.pos.x += self.snelheid_x
        player_rect.x = self.pos.x
        for _, obj_rect in objects:
            if player_rect.colliderect(obj_rect):
                if self.snelheid_x > 0:  # Beweging naar rechts
                    self.pos.x = obj_rect.left - self.PLAYER_WIDTH
                elif self.snelheid_x < 0:  # Beweging naar links
                    self.pos.x = obj_rect.right
                self.snelheid_x = 0

        # Update het rect na de x-beweging
        player_rect.x = self.pos.x

        # Controleer botsing op de y-as
        self.pos.y += self.snelheid_y
        player_rect.y = self.pos.y
        for _, obj_rect in objects:
            if player_rect.colliderect(obj_rect):
                if self.snelheid_y > 0:  # Beweging naar beneden
                    self.pos.y = obj_rect.top - self.PLAYER_HEIGHT
                elif self.snelheid_y < 0:  # Beweging naar boven
                    self.pos.y = obj_rect.bottom
                self.snelheid_y = 0   

    def question_collision(self):
        self.player_rect = pygame.Rect(self.pos.x, self.pos.y, self.PLAYER_WIDTH, self.PLAYER_HEIGHT)
        self.pos.x += self.snelheid_x
        self.player_rect.x = self.pos.x
        questionoo = False
        for ques_rec in vraagbox_lijst:
            if self.player_rect.colliderect(ques_rec):
                questionoo = True
                vraagbox_lijst.remove(ques_rec)
                return questionoo
        return questionoo
    
    def move(self):
        self.pos += pygame.math.Vector2(self.snelheid_x, self.snelheid_y)

    #view functie
    def overlayer(self):
        upper_surface1.set_colorkey((255, 255, 255))
        pygame.draw.circle(upper_surface1, (255, 255, 255), ((self.pos.x + PLAYER_WIDTH/2), (self.pos.y + PLAYER_HEIGHT/2)), 150)
        screen.blit(upper_surface1, (0, 0))

    def update(self):
        self.user_input()
        self.wall_collisions()
        self.move()
        TRUE_OR_FALSE_COLIDE_QUES = self.question_collision()
        self.object_collision()
        self.overlayer()
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        return TRUE_OR_FALSE_COLIDE_QUES
    
class bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        super().__init__()
        self.bulletimage = pygame.image.load("NKPextra/schuim.png").convert_alpha()
        self.bulletimage = pygame.transform.rotozoom(self.bulletimage, 0, 1.4)
        self.image = self.bulletimage
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = BULLET_SPEED
        self.x_vel = self.speed * math.cos(math.radians(angle))
        self.y_vel = -self.speed * math.sin(math.radians(angle))

    def check_collision(self):
        for _, obj_rect in objects:
            if self.rect.colliderect(obj_rect):  # Controleer botsing met objecten
                return True
        for _, vuur_rect in vuur_lijst:
            if self.rect.colliderect(vuur_rect):
                vuur_lijst.remove((_, vuur_rect))
        return False
    
    def update(self):
        self.rect.x += self.x_vel
        self.rect.y += self.y_vel
        # Verwijder de kogel als deze buiten het scherm gaat
        if self.check_collision() or (self.rect.x < 0 or self.rect.x > WIDTH or self.rect.y < 0 or self.rect.y > HEIGHT):
            self.kill()
    
player = Player()
add_questionbox()
bullet_group = pygame.sprite.Group()


#Scoredeel begin
upper_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
upper_surface1 = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
background_surf = pygame.Surface((WIDTH, HEIGHT))
for k in range(i_y):
    pos_y_back = k * y_background
    for l in range(i_x):
        pos_x_back = l * x_background
        background_surf.blit(background, (pos_x_back, pos_y_back))
        upper_surface.blit(background, (pos_x_back, pos_y_back))
for i, j in objects:
    background_surf.blit(i, j)
    upper_surface.blit(i,j)
BLURBACK = pygame.transform.gaussian_blur(upper_surface, 15)
#Scoredeel einde

class producbar():
    def __init__(self, K, L, M, N, max_hp):
        self.K = K
        self.L = L
        self.M = M
        self.N = N 
        self.hp = max_hp # De huidige gezondheid van de speler
        self.max_hp = max_hp  # Maximale gezondheid van de speler

    def update(self):
        global NOTGAMEOVER
        if len(vraagbox_lijst) >= len(vuur_lijst):
            hpdeterminescore = len(vraagbox_lijst)
        else:
            hpdeterminescore = len(vuur_lijst) 
        if hpdeterminescore == 0:
            self.hp = 100
        elif hpdeterminescore == 1:
            self.hp = 90
        elif hpdeterminescore == 2:
            self.hp = 80
        elif hpdeterminescore == 3:
            self.hp = 70
        elif hpdeterminescore == 4:
            self.hp = 60
        elif hpdeterminescore == 5:
            self.hp = 50
        elif hpdeterminescore == 6:
            self.hp = 40
        elif hpdeterminescore == 7:
            self.hp = 30
        elif hpdeterminescore == 8:
            self.hp = 20
        elif hpdeterminescore == 9:
            self.hp = 10
        elif hpdeterminescore == 10:
            self.hp = 0
            NOTGAMEOVER = False

    def draw(self, surface):
        ratio = self.hp / self.max_hp  # Hoeveelheid van de healthbar die moet worden ingevuld
        pygame.draw.rect(surface, "red", (self.K, self.L, self.M, self.N))  # Achtergrond van de healthbar
        pygame.draw.rect(surface, "green", (self.K, self.L, self.M * ratio, self.N))  # Gezondheidsbalk

# Maak een instance van de healthbar met een beginwaarde van 100 HP
produc_bar = producbar((WIDTH - PRODUCBARBREEDTE)/2 , 20, PRODUCBARBREEDTE, PRODUCBARHOOGTE, 100)

#Vuurdeel begin 
vuur_breedte = 55
vuur_hoogte = 55
vuur_lijst = []
vuur_afbeelding = pygame.image.load("NKPGAME/Vlam.png")
vuur_afbeelding = pygame.transform.scale(vuur_afbeelding, (vuur_breedte, vuur_hoogte))
laatste_vuur_spawn = 0
counter1 = 0
def add_vuur():
    x_pos = random.randint(0, WIDTH- vuur_breedte)
    y_pos = random.randint(0, HEIGHT- vuur_hoogte)
    vuur_rect= pygame.Rect(x_pos, y_pos, vuur_breedte, vuur_hoogte)
    if check_valid(vuur_rect):  # Reeds bestaande functie om botsingen te vermijden
            vuur_lijst.append((vuur_afbeelding, vuur_rect))

def spawn_vuur_tijdelijk():
    global laatste_vuur_spawn, counter1
    if counter1 - laatste_vuur_spawn > 50:  # Elke 5 seconden
        add_vuur()
        laatste_vuur_spawn = counter1

def check_vuur_collision(player_rect):
    for vuur_rect in vuur_lijst:
        if player_rect.colliderect(vuur_rect):
            return True
    return False
#vuurdeel einde

#setting scherm
settings_text1 = "In Sollies klaslokaal moet jij, meneer Sollie, \n de orde in de klas zien te houden. Dit kan door vragen \nuit de klas te beantwoorden en af en toe een brandje te blussen. \n  Dit moet zo snel mogelijk, zodat je productiviteitsstreep (midden-boven)\n zo groen mogelijk blijft. Alle vragen uit de klas gaan \n over het rekenen met machten. "
settings_text1_lijst = settings_text1.split("\n")
settings_text2 = """W/A/S/D : bewegen\n
Spatie/Linkermuisknop : schieten\n 
Shift : open settings menu\n """
settings_text2_lijst = settings_text2.split("\n")

settings_text3 = """Deze regels zijn alles wat je nodig hebt \n
om de vragen goed te kunnen beantwoorden:\n\n
Tip 1: '^' betekent 'tot de macht', dus 2^2 = 2 tot de macht 2 = 4\n
Tip 2: '*' betekent 'keer' en / betekent 'gedeeld door'\n\n
a² * a^p = a^(p+q)\n
a^p / a^q = a^(p-q)\n
(a^p)^q = a^(p*q)\n
(ab)^p = a^p * b^p\n
a^0 = 1\n
a^-1 = 1/a\n
a^-p = 1/(a^p)\n
a^½ = √a
"""
settings_text3_lijst = settings_text3.split("\n")

secret_unlocked = False
def draw_settings_content():
    top_text_settings = GROOT_font.render("Settings and Information", True, (0,0,0))
    ESCAPE_text = score_font.render("Klik 'Esc' om terug te gaan", True, (0,0,0))
    mid_text = GROOT_font.render("Controls", True, (0,0,0))
    explaining_text = GROOT_font.render("Uitleg / regels machten", True, (0,0,0))
    screen.blit(top_text_settings, ((WIDTH - top_text_settings.get_width())/2, 10 + PRODUCBARHOOGTE ))
    screen.blit(ESCAPE_text, (WIDTH - ESCAPE_text.get_width() -2, 2))
    for i in range(len(settings_text1_lijst)):
        settings_text1_screen = score_font.render(settings_text1_lijst[i], True, (0,0,0))
        HEIGHT_determine = HEIGHT/6 + (settings_text1_screen.get_height()*i)
        screen.blit(settings_text1_screen, ((WIDTH - settings_text1_screen.get_width())/2, (HEIGHT_determine)))
    control_text_height = HEIGHT_determine + settings_text1_screen.get_height()
    screen.blit(mid_text, ((WIDTH - mid_text.get_width())/2, control_text_height))
    sub_control_text_height = control_text_height + mid_text.get_height()
    for i in range(len(settings_text2_lijst)):
        settings_text2_screen = score_font.render(settings_text2_lijst[i], True, (0,0,0))
        HEIGHT_determine = sub_control_text_height + (settings_text2_screen.get_height()-8) * i
        screen.blit(settings_text2_screen, ((WIDTH - settings_text2_screen.get_width())/2, HEIGHT_determine))
    control_text_height = HEIGHT_determine + settings_text2_screen.get_height()
    screen.blit(explaining_text, ((WIDTH - explaining_text.get_width())/2, control_text_height))
    sub_control_text_height = control_text_height + explaining_text.get_height()
    for i in range(len(settings_text3_lijst)):
        settings_text3_screen = score_font.render(settings_text3_lijst[i], True, (0,0,0))
        HEIGHT_determine = sub_control_text_height + (settings_text3_screen.get_height()-8) * i
        screen.blit(settings_text3_screen, ((WIDTH - settings_text3_screen.get_width())/2, HEIGHT_determine))
#    if secret_unlocked:
#        secret_unlocked_text = score_font.render("Klik nu 'u' om te wisselen van skin", True, (0,0,0))
#        HEIGHT_determine += 20
#        screen.blit(secret_unlocked_text, ((WIDTH - secret_unlocked_text.get_width())/2, HEIGHT_determine))
#        HEIGHT_determine += secret_unlocked_text.get_height() + 10
#        new_text = score_font.render("Selected skin:", True, (0,0,0))
#        screen.blit(new_text, ((WIDTH - new_text.get_width())/2, HEIGHT_determine) )
#        HEIGHT_determine += new_text.get_height() + 10
#        if not player.secret_unlocked:
#            screen.blit(framelijst[0], ((WIDTH - framelijst[0].get_width())/2, HEIGHT_determine))
#        if player.secret_unlocked:
#            screen.blit(kframelijst[0], ((WIDTH - kframelijst[0].get_width())/2, HEIGHT_determine))
#    else:
#        secret_locked_text = score_font.render("Haal meer dan 2000 punten om dit te unlocken:\n\nPersonage: 01001011 01100001 01110011 01110100\n01100101 01101100 01100101 01101001 01101110 ", True, (0,0,0))
#        HEIGHT_determine += 20
#        screen.blit(secret_locked_text, ((WIDTH - secret_locked_text.get_width())/2, HEIGHT_determine))

settings_img = pygame.transform.rotozoom(pygame.image.load("NKPGAME/SHIFT-Photoroom.png"), 0, SETTINGGROOTE)
settingsoo = False 
counter2 = 0
counter1 = 0
key_cooldown = pygame.time.get_ticks()
NOTGAMEOVER = True

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

        text_surface = self.font.render(self.text, True, (0,0,0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_clicked(self, event): 
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos)

#Button
button4 = Button(0, 0, 100, 40, "Home")

while NOTGAMEOVER:
    
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    if settingsoo:
        if keys[pygame.K_ESCAPE]:
            settingsoo = False
        if secret_unlocked:
            timedown = pygame.time.get_ticks()
            if keys[pygame.K_u] and key_cooldown < (timedown - 500): 
                if player.secret_unlocked:
                    key_cooldown = pygame.time.get_ticks()
                    player.secret_unlocked = False
                else: 
                    player.secret_unlocked = True
                    key_cooldown = pygame.time.get_ticks()
        screen.fill(LIGHT_YELLOW)
        draw_settings_content()
        page.blit(screen, (0, blbl.get_height() ))
    elif not questionoo:
        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            settingsoo = True
        screen.blit(background_surf, (0,0))
        for i in range (len(vraagbox_lijst)):
            screen.blit(vraagbox_img, vraagbox_lijst[i])
        screen.blit(player.image, player.pos)
        upper_surface1 =BLURBACK.copy()
        questionoo = player.update()
        bullet_group.update()  # Update alle kogels
        bullet_group.draw(screen)  # Teken alle kogels
        if highscore <= playerscore:
            a = open("highscore.txt", "w")
            a.write(str(playerscore))
            a.close()
            highscore = playerscore
        if highscore >= 2000:
            secret_unlocked = True
        display_score(score_font)
        spawn_vuur_tijdelijk()
        counter2 += 1
        counter1 += 1
        if counter2 == 10:
            counter2 = 0
            playerscore += 1
        if counter1 % 300 == 0:
            add_questionbox()
            for i in vuur_lijst:
                playerscore -= 10
                if playerscore < 0:
                    playerscore = 0
        for i, j in vuur_lijst:
            screen.blit(i, j)
        screen.blit(settings_img, (WIDTH- settings_img.get_width(), 0))
        page.blit(screen, (0, blbl.get_height() ))
    elif questionoo:
        returnedvalue = questiontime()
        if returnedvalue == "SPEL STOPT":
            pygame.quit()
            exit()
        elif returnedvalue == "Vraag goed":
            playerscore += 20
            questionoo = False   
    produc_bar.update()
    produc_bar.draw(page)
    button4.draw(page)
#    if button4.is_clicked(event):
#        main.start_programma()
    pygame.display.update()
    clock.tick(FPS)
pygame.mixer.music.fadeout(500)
pygame.mixer.music.load("NKPGAME/DIESOUND.mp3")
pygame.mixer.music.play(loops=-1, start=0, fade_ms=1000)
pygame.mixer.music.set_volume(1)
videochoice = random.randint(1,2)
print(videochoice)
while True:
    game_over_text = GROOOOT_font.render("YOU COULDN'T\nKEEP ORDER", True, (255, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            exit()
    page.fill((0,0,0))
    if videochoice == 1:
        ret, frame = video.read()
    else:
        ret, frame = video2.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = pygame.surfarray.make_surface(frame)
    frame = pygame.transform.rotate(frame, -90)
    page.blit(frame, ((WIDTH - frame.get_width())/2, (HEIGHT - frame.get_height())/2))
    page.blit(game_over_text, ((WIDTH - game_over_text.get_width())/2, 10))
    pygame.display.update()
    clock.tick(videofps)