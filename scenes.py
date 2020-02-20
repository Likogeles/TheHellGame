import pygame
import time
import random

from classes import HealthPoint, BulletSliderSprite, Button, HeroBut, Dialog_window, Death_image, NewGun
from classes import Floor, Endlevel, Box, Glass
from classes import Bullet, SinusBullet, DownHeroBullet, DownBullet, DubBullet
from classes import Hero, Npc, GoodEnemy, BaseEnemy, UpEnemy, Saw, Boss
from functions import load_image, saving_location, check_continue, check_plot
from dialogues import dialog_with_AGT, dialog_with_ILD, dialog_with_PLN, dialog_with_RSL


class Menu:
    def __init__(self):
        pygame.mixer.music.load("data/Music/themesound.mp3")
        pygame.mixer.music.play()
        self.all_sprites = pygame.sprite.Group()

        sprite = pygame.sprite.Sprite()
        sprite.image = load_image("control.png")
        sprite.rect = sprite.image.get_rect()
        sprite.rect.x = 30
        sprite.rect.y = 300
        self.all_sprites.add(sprite)

        theme = pygame.sprite.Sprite()
        theme.image = load_image("maintheme.png")
        theme.rect = theme.image.get_rect()
        theme.rect.x = 240
        theme.rect.y = 100
        self.all_sprites.add(theme)

        pygame.mouse.set_visible(True)
        self.menu_but_sprites = pygame.sprite.Group()
        if check_continue():
            Button("continue", "continuebut.png", 336, 300, self.menu_but_sprites, self.all_sprites)
        Button("newgame", "newgamebut.png", 336, 360, self.menu_but_sprites, self.all_sprites)
        Button("listlevs_", "levelsbut.png", 336, 420, self.menu_but_sprites, self.all_sprites)
        Button("quit", "quitbut.png", 336, 480, self.menu_but_sprites, self.all_sprites)

    def render(self, screen):
        screen.fill((0, 0, 0))
        self.all_sprites.draw(screen)

    def click(self, pos, scr):
        for i in self.menu_but_sprites:
            if i.click(pos):
                while i.rect.x < 970:
                    for j in self.menu_but_sprites:
                        j.rect.x += 15
                    self.render(scr)
                    pygame.display.flip()
                    time.sleep(0.001)
                return i.name
        return "menu"


class Listlevs:
    def __init__(self):
        self.menu_but_sprites = pygame.sprite.Group()
        Button("level_1", "level_1.png", 336, 240, self.menu_but_sprites)
        if check_plot() >= 1:
            Button("level_2", "level_2.png", 336, 300, self.menu_but_sprites)
        if check_plot() >= 3:
            Button("level_3", "level_3.png", 336, 360, self.menu_but_sprites)
        if check_plot() >= 5:
            Button("level_4", "level_4.png", 336, 420, self.menu_but_sprites)
        Button("menu_", "back.png", 336, 480, self.menu_but_sprites)
        pygame.mixer.music.load("data/Music/themesound.mp3")
        pygame.mixer.music.play()

        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(0.1)

    def render(self, screen):
        screen.fill((0, 0, 0))
        self.menu_but_sprites.draw(screen)

    def click(self, pos, scr):
        for i in self.menu_but_sprites:
            if i.click(pos):
                while i.rect.x < 970:
                    for j in self.menu_but_sprites:
                        j.rect.x += 10
                    self.render(scr)
                    pygame.display.flip()
                    time.sleep(0.001)
                return i.name
        return "listlevs"


class Level:
    def __init__(self, level_text):

        sprite = pygame.sprite.Sprite()
        sprite.image = load_image("control.png")
        sprite.rect = sprite.image.get_rect()
        sprite.rect.x = 100
        sprite.rect.y = 150
        self.control_sprite = pygame.sprite.Group(sprite)

        self.hero_sprites = pygame.sprite.Group()
        self.npc_sprites = pygame.sprite.Group()

        self.floor_sprites = pygame.sprite.Group()
        self.boxes_sprites = pygame.sprite.Group()

        self.enemy_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.dub_bullet_sprites = pygame.sprite.Group()

        self.hp_sprites = pygame.sprite.Group()
        self.herobut_sprites = pygame.sprite.Group()

        self.but_sprites = pygame.sprite.Group()

        self.all_sprites = pygame.sprite.Group()
        self.pause = False
        self.level_text = level_text[:-4].lower()

        self.font = pygame.font.Font(None, 30)
        self.dialog_namefont = pygame.font.Font(None, 65)
        self.dialog_gunfont = pygame.font.Font(None, 50)
        self.dialog_font = pygame.font.Font(None, 30)
        self.dialog_sprites = pygame.sprite.Group()
        self.dialog_sprites.add(Dialog_window())
        self.newgun_sprites = pygame.sprite.Group(NewGun())
        self.death_sprites = pygame.sprite.Group()

        if self.level_text == "level_1":
            Button("continue", "continuebut.png", 336, 360, self.but_sprites)
        else:
            Button("continue", "continuebut.png", 336, 300, self.but_sprites)
            Button(self.level_text, "again.png", 336, 360, self.but_sprites)
        Button("menu_", "exittomenu.png", 336, 420, self.but_sprites)
        Button("quit", "quitbut.png", 336, 480, self.but_sprites)

        self.bullet_0_slider = pygame.sprite.Group(BulletSliderSprite("bull_0_slider.png"))
        self.bullet_1_slider = pygame.sprite.Group(BulletSliderSprite("bull_1_slider.png"))
        self.bullet_2_slider = pygame.sprite.Group(BulletSliderSprite("bull_2_slider.png"))
        self.bullet_3_slider = pygame.sprite.Group(BulletSliderSprite("bull_3_slider.png"))

        self.bullet_shoot_sound = pygame.mixer.Sound("data/Sounds/bullet.ogg")
        self.bullet_shoot_sound.set_volume(0.15)
        self.down_bullet_shoot_sound = pygame.mixer.Sound("data/Sounds/down_bullet.ogg")

        self.bullet_damage_sound = pygame.mixer.Sound("data/Sounds/BaseEnemyDamage.ogg")
        self.bullet_damage_sound.set_volume(0.15)
        self.bulletdown_damage_sound = pygame.mixer.Sound("data/Sounds/DownBulletDamage.ogg")
        self.bulletdown_damage_sound.set_volume(0.5)
        self.dubbullet_sound = pygame.mixer.Sound("data/Sounds/The Living Tombstone - Spooky scary skeleton.ogg")
        self.dubbullet_sound.set_volume(0.25)
        self.glass_break_sound = pygame.mixer.Sound("data/Sounds/break.ogg")
        self.glass_break_sound.set_volume(0.5)
        self.death_sound = pygame.mixer.Sound("data/Sounds/death.ogg")
        self.death_sound.set_volume(0.5)

        self.boss = None

        filename = "data/LevelsLists/" + level_text
        with open(filename, 'r') as mapFile:
            level_map = [line.strip() for line in mapFile]
        max_width = max(map(len, level_map))
        level = list(map(lambda x: x.ljust(max_width, '.'), level_map))

        for i in range(len(level)):
            for j in range(len(level[0])):
                if level[i][j] == "0":
                    x = Box(50 * j, 50 * i, self.boxes_sprites)
                    self.all_sprites.add(x)
                    self.floor_sprites.add(x)
                elif level[i][j] == "G":
                    x = Glass(50 * j, 50 * i, self.boxes_sprites)
                    self.all_sprites.add(x)
                    self.floor_sprites.add(x)
                elif level[i][j] == "@":
                    self.hero = Hero(50 * j, 50 * i - 40, self.hero_sprites)
                elif level[i][j] == "#":
                    self.all_sprites.add(BaseEnemy(50 * j, 50 * i - 40, self.enemy_sprites))
                elif level[i][j] == "&":
                    self.all_sprites.add(UpEnemy(50 * j, 50 * i, self.enemy_sprites))
                elif level[i][j] == "-":
                    self.all_sprites.add(GoodEnemy(50 * j, 50 * i - 40, self.enemy_sprites))
                elif level[i][j] == "_":
                    self.all_sprites.add(Saw(50 * j, 50 * i + 10, self.enemy_sprites))
                elif level[i][j] == "B":
                    if check_plot() == 6:
                        self.boss = Boss(self.enemy_sprites)
                        self.all_sprites.add(self.boss)

    def render(self, screen):
        screen.fill((0, 0, 0))
        self.all_sprites.draw(screen)
        self.hp_sprites.draw(screen)

        x = self.hero.hero_check_npc(self.npc_sprites)
        if x:
            x.dialog = True
            screen.blit(self.font.render(x.name, 1, (255, 255, 255)), (x.rect.x - 25, x.rect.y - 41))
            HeroBut(x.rect.x + 15, x.rect.y - 20, self.herobut_sprites)
        self.herobut_sprites.draw(screen)
        self.herobut_sprites = pygame.sprite.Group()

        self.bullet_sprites.draw(screen)

        self.hero_sprites.draw(screen)
        if self.hero.weapons_slide == 0:
            self.dubbullet_sound.stop()
            for i in self.dub_bullet_sprites:
                i.kill()
            self.bullet_0_slider.draw(screen)
        elif self.hero.weapons_slide == 1:
            self.dubbullet_sound.stop()
            for i in self.dub_bullet_sprites:
                i.kill()
            self.bullet_1_slider.draw(screen)
        elif self.hero.weapons_slide == 2:
            self.dubbullet_sound.stop()
            for i in self.dub_bullet_sprites:
                i.kill()
            self.bullet_2_slider.draw(screen)
        elif self.hero.weapons_slide == 3:
            self.bullet_3_slider.draw(screen)

        self.dub_bullet_sprites.draw(screen)

        if self.pause:
            self.hero.stop_all_move()
            self.dubbullet_sound.stop()
            for i in self.dub_bullet_sprites:
                i.kill()
            self.bullet_1_slider.draw(screen)
            pygame.mouse.set_visible(True)
            self.but_sprites.draw(screen)
            self.control_sprite.draw(screen)

            if self.hero.weapons_slide == 0:
                self.bullet_0_slider.draw(screen)
            elif self.hero.weapons_slide == 1:
                self.bullet_1_slider.draw(screen)
            elif self.hero.weapons_slide == 2:
                self.bullet_2_slider.draw(screen)
            elif self.hero.weapons_slide == 3:
                self.bullet_3_slider.draw(screen)
        else:
            pygame.mouse.set_visible(False)
            if self.boss:
                if not self.boss.life:
                    pygame.mixer.music.stop()
                    self.boss.explosion(screen)

    def death(self, screen):
        self.death_sprites.add(Death_image(self.hero.rect.x - 45, self.hero.rect.y, "Hero/death_0.png"))
        for r in range(10, 1000, 5):
            x = self.hero.rect.x + 25
            y = self.hero.rect.y + 45
            screen.fill((0, 0, 0))
            self.render(screen)
            pygame.draw.circle(screen, (0, 0, 255), (x, y), r)
            pygame.draw.circle(screen, (0, 0, 0), (x, y), r - 10)
            if r % 125 == 0:
                for i in self.death_sprites:
                    i.kill()
                self.death_sprites.add(Death_image(self.hero.rect.x - 45, self.hero.rect.y, "Hero/death_" + str(r // 125) + ".png"))
            self.death_sprites.draw(screen)
            pygame.display.flip()

    def gravity(self, screen):
        if not self.pause:
            self.hero.gravity(self.floor_sprites, self.all_sprites)

            for i in self.bullet_sprites:
                x = i.fly(self.all_sprites, self.hero_sprites)

                if type(x) == int:
                    if x <= 0:
                        for j in self.enemy_sprites:
                            if type(j) == Saw:
                                j.saw_sound.stop()
                        self.dubbullet_sound.stop()
                        pygame.mixer.music.stop()
                        self.death_sound.play()
                        self.death(screen)
                        return self.level_text
                elif x == "damage":
                    self.bullet_damage_sound.play()
                elif x == "damagedown":
                    self.bulletdown_damage_sound.play()
            for i in self.dub_bullet_sprites:
                x = i.fly(self.all_sprites, self.hero_sprites)
                if x == "break":
                    self.glass_break_sound.play()

            for i in self.hp_sprites:
                i.kill()
            for i in range(self.hero.hp):
                if i % 10 == 0:
                    HealthPoint((i // 10) * 40 + 10, 10, self.hp_sprites)

    def movingupdate(self, screen):
        if not self.pause:
            for i in self.enemy_sprites:
                x = i.moving(self.floor_sprites, self.hero_sprites)
                if x:
                    if type(x) == Bullet:
                        self.bullet_shoot_sound.play()
                        self.bullet_sprites.add(x)
                        self.all_sprites.add(x)
                    elif type(x) == DownBullet:
                        self.down_bullet_shoot_sound.play()
                        self.bullet_sprites.add(x)
                        self.all_sprites.add(x)
                    elif type(x) == Hero:
                        if x.hp <= 0:
                            self.dubbullet_sound.stop()
                            for i in self.enemy_sprites:
                                if type(i) == Saw:
                                    i.saw_sound.stop()
                            pygame.mixer.music.stop()
                            self.death_sound.play()
                            self.death(screen)
                            return self.level_text
            for i in self.npc_sprites:
                i.moving(self.floor_sprites)

    def animateupdate(self):
        if not self.pause:
            self.hero.animate()

    def enemyanimateupdate(self):
        if not self.pause:
            for i in self.enemy_sprites:
                i.animate()

    def eventupdate(self, event, screen):

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.pause = not self.pause

        if self.pause:
            if event.type == pygame.MOUSEBUTTONDOWN:
                x = self.click(event.pos)
                if x == "continue":
                    self.pause = not self.pause
                else:
                    self.dubbullet_sound.stop()
                    for i in self.enemy_sprites:
                        if type(i) == Saw:
                            i.saw_sound.stop()
                    return x
        else:
            x = self.hero.eventin(event, self.floor_sprites, self.all_sprites, self.npc_sprites)
            if x:
                if type(x) == Bullet or type(x) == SinusBullet or type(x) == DownHeroBullet:
                    self.bullet_sprites.add(x)
                    if type(x) == Bullet:
                        self.bullet_shoot_sound.play()
                    elif type(x) == DownHeroBullet:
                        self.down_bullet_shoot_sound.play()
                elif x == "DubBulletadd":
                    self.dubbullet_sound.play(-1)
                    if self.hero.oldrunningwasright:
                        self.dub_bullet_sprites.add(DubBullet(self.hero.rect.x + 50, self.hero.rect.y - 20, self.hero.oldrunningwasright))
                    else:
                        self.dub_bullet_sprites.add(DubBullet(self.hero.rect.x - 95, self.hero.rect.y - 20, self.hero.oldrunningwasright))
                elif x == "DubBulletremove":
                    self.dubbullet_sound.stop()
                    for i in self.dub_bullet_sprites:
                        i.kill()
                elif x == "level_1" or x == "level_2" or x == "level_3" or x == "level_4" or x == "level_5" or x == "menu_":
                    for i in self.enemy_sprites:
                        if type(i) == Saw:
                            i.saw_sound.stop()
                    self.dubbullet_sound.stop()
                    return x
                elif x[:12] == "dialogwindow":
                    self.dubbullet_sound.stop()
                    for i in self.dub_bullet_sprites:
                        i.kill()
                    self.hero.stop_all_move()
                    self.render(screen)
                    y = None
                    if x[12:] == "АГТ2v512":
                        y = dialog_with_AGT(self, screen, x)
                    elif x[12:] == "ИЛД1v108":
                        y = dialog_with_ILD(self, screen, x)
                    elif x[12:] == "ПЛН0v105":
                        y = dialog_with_PLN(self, screen, x)
                    elif x[12:] == "РСЛ1v410":
                        y = dialog_with_RSL(self, screen, x)
                    if y:
                        for i in self.enemy_sprites:
                            if type(i) == Saw:
                                i.saw_sound.stop()
                        self.dubbullet_sound.stop()
                        return y

    def hero_shoot(self):
        x = self.hero.shoot()
        if x:
            if type(x) == Bullet or type(x) == SinusBullet or type(x) == DownHeroBullet:
                self.bullet_sprites.add(x)

    def click(self, pos):
        for i in self.but_sprites:
            if i.click(pos):
                return i.name
        return ''.join(self.level_text.split("_"))


class Level1(Level):
    def __init__(self, level_text):
        super().__init__(level_text)
        saving_location(1)
        pygame.mixer.music.load("data/Music/themesound.mp3")
        pygame.mixer.music.play()

        filename = "data/LevelsLists/" + level_text
        with open(filename, 'r') as mapFile:
            level_map = [line.strip() for line in mapFile]
        max_width = max(map(len, level_map))
        level = list(map(lambda x: x.ljust(max_width, '.'), level_map))

        num_of_npc = 0
        num_of_level = 0

        for i in range(len(level)):
            for j in range(len(level[0])):
                if level[i][j] == "=":
                    self.all_sprites.add(Floor(50 * j, 50 * i, "Hub/floor_" + str(random.randint(0, 11)) + ".png", self.floor_sprites))
                elif level[i][j] == "N":
                    if num_of_npc == 0:
                        if check_plot() >= 1:
                            self.all_sprites.add(Npc(50 * j, 50 * i - 20, "ИЛД1v108", self.npc_sprites))
                    elif num_of_npc == 1:
                        if check_plot() >= 3:
                            self.all_sprites.add(Npc(50 * j, 50 * i - 20, "ПЛН0v105", self.npc_sprites))
                    elif num_of_npc == 2:
                        self.all_sprites.add(Npc(50 * j, 50 * i - 20, "АГТ2v512", self.npc_sprites))
                    elif num_of_npc == 3:
                        if check_plot() >= 5:
                            self.all_sprites.add(Npc(50 * j, 50 * i - 20, "РСЛ1v410", self.npc_sprites))
                    num_of_npc += 1
                elif level[i][j] == "+":
                    if num_of_level == 0:
                        Endlevel(50 * j, 50 * i - 50, "level_2", "level1.png", self.all_sprites)
                    elif num_of_level == 1:
                        Endlevel(50 * j, 50 * i - 50, "level_3", "level1.png", self.all_sprites)
                    elif num_of_level == 2:
                        Endlevel(50 * j, 50 * i - 50, "level_4", "level1.png", self.all_sprites)
                    elif num_of_level == 3:
                        Endlevel(50 * j, 50 * i - 50, "level_5", "level1.png", self.all_sprites)
                    num_of_level += 1


class Level2(Level):
    def __init__(self, level_text):
        super().__init__(level_text)
        saving_location(2)
        pygame.mixer.music.load("data/Music/level2.mp3")
        pygame.mixer.music.play()

        filename = "data/LevelsLists/" + level_text
        with open(filename, 'r') as mapFile:
            level_map = [line.strip() for line in mapFile]
        max_width = max(map(len, level_map))
        level = list(map(lambda x: x.ljust(max_width, '.'), level_map))

        for i in range(len(level)):
            for j in range(len(level[0])):
                if level[i][j] == "=":
                    self.all_sprites.add(Floor(50 * j, 50 * i, "MathHell/floor_" + str(random.randint(0, 18)) + ".png", self.floor_sprites))
                elif level[i][j] == "N":
                    if check_plot() == 0:
                        self.all_sprites.add(Npc(50 * j, 50 * i - 20, "ИЛД1v108", self.npc_sprites))
                elif level[i][j] == "+":
                    Endlevel(50 * j, 50 * i - 50, "level_1", "level1.png", self.all_sprites)


class Level3(Level):
    def __init__(self, level_text):
        super().__init__(level_text)
        saving_location(3)
        pygame.mixer.music.load("data/Music/level3.mp3")
        pygame.mixer.music.play(-1)

        filename = "data/LevelsLists/" + level_text
        with open(filename, 'r') as mapFile:
            level_map = [line.strip() for line in mapFile]
        max_width = max(map(len, level_map))
        level = list(map(lambda x: x.ljust(max_width, '.'), level_map))

        for i in range(len(level)):
            for j in range(len(level[0])):
                if level[i][j] == "=":
                    self.all_sprites.add(Floor(50 * j, 50 * i, "MedHell/floor_" + str(random.randint(0, 7)) + ".png", self.floor_sprites))
                elif level[i][j] == "N":
                    if check_plot() == 2:
                        self.all_sprites.add(Npc(50 * j, 50 * i - 20, "ПЛН0v105", self.npc_sprites))
                elif level[i][j] == "+":
                    Endlevel(50 * j, 50 * i - 50, "level_1", "level1.png", self.all_sprites)


class Level4(Level):
    def __init__(self, level_text):
        super().__init__(level_text)
        saving_location(4)
        pygame.mixer.music.load("data/Music/level4.mp3")
        pygame.mixer.music.play(-1)

        filename = "data/LevelsLists/" + level_text
        with open(filename, 'r') as mapFile:
            level_map = [line.strip() for line in mapFile]
        max_width = max(map(len, level_map))
        level = list(map(lambda x: x.ljust(max_width, '.'), level_map))

        for i in range(len(level)):
            for j in range(len(level[0])):
                if level[i][j] == "=":
                    self.all_sprites.add(Floor(50 * j, 50 * i, "MusHell/floor_" + str(random.randint(0, 7)) + ".png", self.floor_sprites))
                elif level[i][j] == "N":
                    if check_plot() == 4:
                        self.all_sprites.add(Npc(50 * j, 50 * i - 20, "РСЛ1v410", self.npc_sprites))
                elif level[i][j] == "+":
                    Endlevel(50 * j, 50 * i - 50, "level_1", "level1.png", self.all_sprites)


class Level5(Level):
    def __init__(self, level_text):
        super().__init__(level_text)
        saving_location(5)
        if check_plot() == 6:
            pygame.mixer.music.load("data/Music/level5.mp3")
            pygame.mixer.music.play(-1)
        else:
            pygame.mixer.music.stop()

        filename = "data/LevelsLists/" + level_text
        with open(filename, 'r') as mapFile:
            level_map = [line.strip() for line in mapFile]
        max_width = max(map(len, level_map))
        level = list(map(lambda x: x.ljust(max_width, '.'), level_map))

        for i in range(len(level)):
            for j in range(len(level[0])):
                if level[i][j] == "=":
                    self.all_sprites.add(Floor(50 * j, 50 * i, "MusHell/floor_" + str(random.randint(0, 7)) + ".png", self.floor_sprites))
                elif level[i][j] == "N":
                    if check_plot() == 4:
                        self.all_sprites.add(Npc(50 * j, 50 * i - 20, "РСЛ1v410", self.npc_sprites))
                elif level[i][j] == "+":
                    Endlevel(50 * j, 50 * i - 50, "level_1", "level1.png", self.all_sprites)
