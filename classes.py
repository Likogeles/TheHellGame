import pygame
import math

from functions import load_image, self_on_screen, check_block, check_npc, check_hero, check_hero_down, check_saves_guns, saving_plot


class HealthPoint(pygame.sprite.Sprite):
    def __init__(self, x, y, *group):
        super().__init__(*group)
        self.image = load_image("Hero/healthpoint.png", -1)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Button(pygame.sprite.Sprite):
    def __init__(self, name, imagename, x, y, *group):
        super().__init__(*group)
        self.image = load_image("Buttons/" + imagename)
        self.rect = self.image.get_rect()
        self.w, self.h = self.image.get_rect()[2], self.image.get_rect()[3]
        self.rect.x = x
        self.rect.y = y
        self.name = name
        self.click_sound = pygame.mixer.Sound("data/Sounds/odd.wav")
        self.click_sound.set_volume(0.4)

    def click(self, pos):
        if self.rect.x <= pos[0] <= self.rect.x + self.w and \
                self.rect.y <= pos[1] <= self.rect.y + self.h:
            self.click_sound.play()
            return True
        return False


class HeroBut(pygame.sprite.Sprite):
    def __init__(self, x, y, *group):
        super().__init__(*group)
        self.image = load_image("Buttons/herobut_e.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Floor(pygame.sprite.Sprite):
    def __init__(self, x, y, imgname, *group):
        super().__init__(*group)
        self.image = load_image("Floor/" + imgname, -1)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Box(Floor):
    def __init__(self, x, y, *group):
        super().__init__(x, y, "box.png", *group)
        self.hp = 100
        self.t = 0

    def get_hit(self, damage):
        if self.t == 0:
            self.rect.x += 2
        elif self.t == 1:
            self.rect.x -= 2
        elif self.t == 2:
            self.rect.x -= 2
        elif self.t == 3:
            self.rect.x += 2
        self.t += 1
        if self.t > 3:
            self.t = 0

        self.hp -= damage
        if self.hp <= 0:
            self.kill()


class Glass(Floor):
    def __init__(self, x, y, *group):
        super().__init__(x, y, "Glass\glass_0.png", *group)
        self.images = [load_image("Floor\Glass\glass_0.png", -1),
                       load_image("Floor\Glass\glass_1.png", -1),
                       load_image("Floor\Glass\glass_2.png", -1),
                       load_image("Floor\Glass\glass_3.png", -1),
                       load_image("Floor\Glass\glass_4.png", -1)]
        self.hp = 1000
        self.t = 0

    def get_hit(self, damage):
        if self.t == 0:
            self.rect.x += 1
        elif self.t == 1:
            self.rect.x -= 1
        elif self.t == 2:
            self.rect.x -= 1
        elif self.t == 3:
            self.rect.x += 1
        self.t += 1
        if self.t > 3:
            self.t = 0

        self.hp -= damage
        if 600 < self.hp <= 800:
            self.image = self.images[1]
        elif 400 < self.hp <= 600:
            self.image = self.images[2]
        elif 200 < self.hp <= 400:
            self.image = self.images[3]
        elif 0 < self.hp <= 200:
            self.image = self.images[4]
        if self.hp <= 0:
            self.kill()


class Endlevel(pygame.sprite.Sprite):
    def __init__(self, x, y, name_of_next_level, imgname, *group):
        super().__init__(*group)
        self.image = load_image("Endsoflevels/" + imgname, -1)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.nextlevel = name_of_next_level


class Dialog_window(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.image = load_image("dialog_window.png", -1)
        self.rect = self.image.get_rect()
        self.rect.x = 86
        self.rect.y = 270


class NewGun(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.image = load_image("newgun.png", -1)
        self.rect = self.image.get_rect()
        self.rect.x = 186
        self.rect.y = 76


class Death_image(pygame.sprite.Sprite):
    def __init__(self, x, y, image, *group):
        super().__init__(*group)
        self.image = pygame.transform.scale(load_image(image, -1), (90, 90))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class BulletSliderSprite(pygame.sprite.Sprite):
    def __init__(self, imgname, *group):
        super().__init__(*group)
        self.image = load_image("Bullets/" + imgname, -1)
        self.rect = self.image.get_rect()
        self.rect.x = 10
        self.rect.y = 40


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, move_on_right, speed, imgname="bull_0.png", *group):
        super().__init__(*group)
        self.image = load_image("Bullets/" + imgname, -1)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move = -speed
        if move_on_right:
            self.move = speed

    def fly(self, all_sprites, hero_sprites):
        self.rect.x += self.move
        if not (-100 <= self.rect.x <= 1000):
            self.kill()
        x = pygame.sprite.spritecollideany(self, all_sprites)
        if x:
            if type(x) == BaseEnemy or type(x) == Box or type(x) == Boss:
                x.get_hit(20)
                self.kill()
                return "damage"
            elif type(x) == Floor or type(x) == Glass:
                self.kill()
                return "damage"

        x = pygame.sprite.spritecollideany(self, hero_sprites)
        if x:
            if type(x) == Hero:
                x.get_hit(20)
                self.kill()
                return x.hp


class SinusBullet(Bullet):
    def __init__(self, x, y, move_on_right, speed, *group):
        super().__init__(x, y, move_on_right, speed, "bull_1.png", *group)
        self.move = - math.pi * 2
        if move_on_right:
            self.move = -self.move
        self.oldx = x
        self.oldy = y

    def fly(self, all_sprites, hero_sprites):
        self.rect.y = self.oldy + int(math.sin((self.rect.x - self.oldx) // 18) * 22)
        self.rect.x += self.move
        if not (-100 <= self.rect.x <= 1000):
            self.kill()
        x = pygame.sprite.spritecollideany(self, all_sprites)
        if x:
            if type(x) == BaseEnemy or type(x) == Box or type(x) == Boss:
                x.get_hit(5)
                self.kill()
                return "damage"
            elif type(x) == Floor or type(x) == Glass:
                self.kill()
                return "damage"


class DownBullet(Bullet):
    def __init__(self, x, y, speed, *group):
        super().__init__(x, y, False, speed, "bull_2.png", *group)
        self.image = load_image("Bullets/" + "bull_2.png", -1)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move = speed

    def fly(self, all_sprites, hero_sprites):
        self.rect.y += self.move
        if not (self.rect.y <= 600):
            self.kill()
        x = pygame.sprite.spritecollideany(self, all_sprites)
        if x:
            if type(x) == BaseEnemy or type(x) == Box:
                x.get_hit(50)
                self.kill()
                return "damagedown"
            elif type(x) == Floor:
                self.kill()
                return "damagedown"

        x = pygame.sprite.spritecollideany(self, hero_sprites)
        if x:
            if type(x) == Hero:
                x.get_hit(50)
                self.kill()
                return x.hp


class DownHeroBullet(Bullet):
    def __init__(self, x, y, speedx, speedy, move_on_right, *group):
        super().__init__(x, y, False, speedy, "bull_2.png", *group)
        self.image = load_image("Bullets/" + "bull_2.png", -1)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.movex = -speedx
        if move_on_right:
            self.movex = speedx
        self.movey = -speedy

    def fly(self, all_sprites, hero_sprites):
        self.rect.x += self.movex
        self.rect.y += self.movey
        self.movey += 0.1
        if not (self.rect.y <= 600) or not (-50 <= self.rect.x <= 972):
            self.kill()
        x = pygame.sprite.spritecollideany(self, all_sprites)
        if x:
            if type(x) == BaseEnemy or type(x) == Box or type(x) == Boss:
                x.get_hit(50)
                self.kill()
                return "damagedown"
            elif type(x) == Floor or type(x) == Glass:
                self.kill()
                return "damagedown"


class DubBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, move_on_right, *group):
        super().__init__(*group)
        self.right_images = [load_image("Bullets/bull_3_0.png", -1), load_image("Bullets/bull_3_1.png", -1),
                             load_image("Bullets/bull_3_2.png", -1), load_image("Bullets/bull_3_3.png", -1),
                             load_image("Bullets/bull_3_4.png", -1)]
        self.left_images = [pygame.transform.flip(load_image("Bullets/bull_3_0.png", -1), True, False),
                            pygame.transform.flip(load_image("Bullets/bull_3_1.png", -1), True, False),
                            pygame.transform.flip(load_image("Bullets/bull_3_2.png", -1), True, False),
                            pygame.transform.flip(load_image("Bullets/bull_3_3.png", -1), True, False),
                            pygame.transform.flip(load_image("Bullets/bull_3_4.png", -1), True, False)]
        if move_on_right:
            self.image = self.right_images[0]
        else:
            self.image = self.left_images[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.t = 0

    def fly(self, all_sprites, hero_sprites):
        if [i for i in hero_sprites]:
            y = [i for i in hero_sprites][0]

            self.t += 1
            if self.t >= 20:
                self.t = 0
            if self.t == 0:
                self.image = self.right_images[0] if y.oldrunningwasright else self.left_images[0]
            elif self.t == 4:
                self.image = self.right_images[1] if y.oldrunningwasright else self.left_images[1]
            elif self.t == 8:
                self.image = self.right_images[2] if y.oldrunningwasright else self.left_images[2]
            elif self.t == 12:
                self.image = self.right_images[3] if y.oldrunningwasright else self.left_images[3]
            elif self.t == 16:
                self.image = self.right_images[4] if y.oldrunningwasright else self.left_images[4]

            self.rect.y = y.rect.y - 20
            self.rect.x = y.rect.x - 95
            if y.oldrunningwasright:
                self.rect.x = y.rect.x + 50

            x = pygame.sprite.spritecollideany(self, all_sprites)
            if x:
                if type(x) == BaseEnemy or type(x) == Box:
                    x.get_hit(10)
                elif type(x) == Glass:
                    x.get_hit(10)
                    if x.hp <= 0:
                        return "break"
                    return "tresk"


class Person(pygame.sprite.Sprite):
    def __init__(self, x, y, imgname, *group):
        super().__init__(*group)
        self.image = load_image(imgname, -1)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.oldrunningwasright = True
        self.hp = 100
        self.immortal = False

    def get_hit(self, damage):
        if not self.immortal:
            self.hp -= damage
            if self.hp <= 0:
                self.kill()


class Npc(Person):
    def __init__(self, x, y, name, *group):
        super().__init__(x, y, "Npces/robot.png", *group)
        self.name = name
        self.dialog = False

    def moving(self, floor_sprites):
        if not self.dialog:
            if self_on_screen(self):
                if self.oldrunningwasright:
                    if check_block(self.rect.x + 45, self.rect.y + 70, floor_sprites) and\
                            not(check_block(self.rect.x + 45, self.rect.y + 20, floor_sprites)):
                        self.rect.x += 1
                    else:
                        self.oldrunningwasright = False
                else:
                    if check_block(self.rect.x - 10, self.rect.y + 70, floor_sprites) and\
                            not (check_block(self.rect.x - 10, self.rect.y + 20, floor_sprites)):
                        self.rect.x -= 1
                    else:
                        self.oldrunningwasright = True
        self.dialog = False


class Hero(Person):
    def __init__(self, x, y, *group):
        super().__init__(x, y, "Hero/hero_0.png", *group)

        self.weapons_slide = 0
        self.shooting_log = False

        self.gravity_acceleration = 0
        self.gravity_log = True

        self.max_point_level_poisk_log = True
        self.min_point_level = [0, 0]
        self.max_point_level = [50, 50]

        self.sinusbullet_shoot_sound = pygame.mixer.Sound("data/Sounds/sinus_bullet.ogg")
        self.sinusbullet_shoot_sound.set_volume(0.1)

        self.t = 0
        self.standing_right = []
        for i in range(8):
            self.standing_right.append(pygame.transform.scale(load_image("Hero/standing_" + str(i) + ".png", -1), (45, 90)))
        self.standing_left = []
        for i in range(8):
            x = pygame.transform.scale(load_image("Hero/standing_" + str(i) + ".png", -1), (45, 90))
            self.standing_left.append(pygame.transform.flip(x, True, False))
        self.running_right = []
        for i in range(8):
            self.running_right.append(pygame.transform.scale(load_image("Hero/running_" + str(i) + ".png", -1), (45, 90)))
        self.running_left = []
        for i in range(8):
            x = pygame.transform.scale(load_image("Hero/running_" + str(i) + ".png", -1), (45, 90))
            self.running_left.append(pygame.transform.flip(x, True, False))

        self.right_move = False
        self.left_move = False

    def animate(self):
        if self.right_move:
            self.image = self.running_right[self.t]
            self.t += 1
            if self.t > 7:
                self.t = 0
            self.oldrunningwasright = True
        elif self.left_move:
            self.image = self.running_left[self.t]
            self.t += 1
            if self.t > 7:
                self.t = 0
            self.oldrunningwasright = False
        else:
            if self.oldrunningwasright:
                self.image = self.standing_right[self.t]
                self.t += 1
                if self.t > 7:
                    self.t = 0
            else:
                self.image = self.standing_left[self.t]
                self.t += 1
                if self.t > 7:
                    self.t = 0

    def move(self, floor_sprites, all_sprites):
        if self.max_point_level_poisk_log:
            self.max_point_level_poisk_log = False
            maxx = 0
            maxy = 0
            for i in all_sprites:
                if i.rect.x > maxx:
                    maxx = i.rect.x
                if i.rect.y > maxy:
                    maxy = i.rect.y
            self.max_point_level = [maxx, maxy]

        sp = 0
        if self.right_move:
            self.rect.x += 2
            if not(pygame.sprite.spritecollideany(self, floor_sprites)):
                sp = -2
            self.rect.x -= 2
            self.gravity_log = True
        elif self.left_move:
            self.rect.x -= 2
            if not(pygame.sprite.spritecollideany(self, floor_sprites)):
                sp = 2
            self.rect.x += 2
            self.gravity_log = True

        if sp != 0:
            if self.rect.x != 486:
                if 0 <= self.rect.x - sp <= 922:
                    self.rect.x -= sp
            else:
                if self.min_point_level[0] + sp > 0 or self.max_point_level[0] + sp < 922:
                    if 0 <= self.rect.x - sp <= 922:
                        self.rect.x -= sp
                else:
                    self.min_point_level[0] += sp
                    self.max_point_level[0] += sp
                    for i in all_sprites:
                        i.rect.x += sp

    def gravity(self, floor_sprites, all_sprites):

        if self.max_point_level_poisk_log:
            self.max_point_level_poisk_log = False
            maxx = 0
            maxy = 0
            for i in all_sprites:
                if i.rect.x >= maxx:
                    maxx = i.rect.x
                if i.rect.y >= maxy:
                    maxy = i.rect.y
            self.max_point_level = [maxx, maxy]

        sp = 1 + int(self.gravity_acceleration)

        self.rect.y += sp
        if pygame.sprite.spritecollideany(self, floor_sprites) or not(0 <= self.rect.y <= 510):
            self.gravity_log = False
            self.rect.y -= sp
            self.gravity_acceleration = 0
        else:
            self.gravity_log = True
            self.rect.y -= sp

        if self.gravity_log:
            if 250 <= self.rect.y <= 260 and self.min_point_level[1] - sp <= 0 and self.max_point_level[1] - sp >= 550:
                self.min_point_level[1] -= sp
                self.max_point_level[1] -= sp
                for i in all_sprites:
                    i.rect.y -= sp
            else:
                self.rect.y += sp

            self.gravity_acceleration += 0.1

            if self.gravity_acceleration > 5:
                self.gravity_acceleration = 5

    def shoot(self):
        if self.shooting_log:
            if self.weapons_slide == 1:
                x = self.rect.x
                if self.oldrunningwasright:
                    x += 50
                else:
                    x -= 25
                return SinusBullet(x, self.rect.y + 35, self.oldrunningwasright, 10)

    def hero_check_npc(self, npc_sprites):
        return check_npc(self.rect.x, self.rect.y, npc_sprites)

    def eventin(self, event, floor_sprites, all_sprites, npc_sprites):
        if self.hp > 0:
            new_bullet = None
            if event.type == pygame.KEYDOWN:
                if pygame.key.get_pressed()[pygame.K_1] and \
                    pygame.key.get_pressed()[pygame.K_2] and \
                     pygame.key.get_pressed()[pygame.K_4]:
                    if not self.immortal:
                        self.immortal = True
                        print("immortal activated")
                    else:
                        self.immortal = False
                        print("immortal disactivated")

                if event.key == pygame.K_e:
                    x = check_npc(self.rect.x, self.rect.y, npc_sprites)
                    if x:
                        return "dialogwindow" + x.name
                elif event.key == pygame.K_d or event.key == pygame.K_a or event.key == pygame.K_SPACE:
                    self.beginmove(event, floor_sprites)
                elif event.key == pygame.K_j:
                    self.beginmove(event, floor_sprites)
                    x = self.rect.x
                    if self.weapons_slide == 0:
                        if self.oldrunningwasright:
                            x += 50
                        else:
                            x -= 25
                        new_bullet = Bullet(x, self.rect.y + 10, self.oldrunningwasright, 10)
                    elif self.weapons_slide == 1:
                        self.sinusbullet_shoot_sound.play(-1)
                    elif self.weapons_slide == 2:
                        if self.oldrunningwasright:
                            x += 50
                        else:
                            x -= 50
                        new_bullet = DownHeroBullet(x, self.rect.y + 10, 2, 2, self.oldrunningwasright)
                    elif self.weapons_slide == 3:
                        if self.oldrunningwasright:
                            x += 50
                        else:
                            x -= 50
                        return "DubBulletadd"
                elif event.key == pygame.K_i:
                    self.sinusbullet_shoot_sound.stop()
                    self.weapons_slide = 0
                elif event.key == pygame.K_o:
                    if check_saves_guns() >= 1:
                        self.weapons_slide = 1
                elif event.key == pygame.K_k:
                    if check_saves_guns() >= 2:
                        self.sinusbullet_shoot_sound.stop()
                        self.weapons_slide = 2
                elif event.key == pygame.K_l:
                    if check_saves_guns() >= 3:
                        self.sinusbullet_shoot_sound.stop()
                        self.weapons_slide = 3
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_d or event.key == pygame.K_a:
                    self.stopmove(event)
                elif event.key == pygame.K_j:
                    if self.weapons_slide == 3:
                        return "DubBulletremove"
                    else:
                        self.stopmove(event)

            self.move(floor_sprites, all_sprites)
            if new_bullet:
                return new_bullet

            x = pygame.sprite.spritecollideany(self, all_sprites)
            if type(x) == Endlevel:
                return x.nextlevel
            return None

    def beginmove(self, event, floor_sprites):
        if event.key == pygame.K_d:
            self.right_move = True
            self.left_move = False
            self.gravity_log = True
        elif event.key == pygame.K_a:
            self.left_move = True
            self.right_move = False
            self.gravity_log = True
        elif event.key == pygame.K_j:
            self.shooting_log = True
        elif event.key == pygame.K_SPACE:
            self.rect.y += 1
            if pygame.sprite.spritecollideany(self, floor_sprites):
                self.gravity_acceleration = -7
            self.rect.y -= 1

    def stopmove(self, event):
        if event.key == pygame.K_d:
            self.right_move = False
        elif event.key == pygame.K_a:
            self.left_move = False
        elif event.key == pygame.K_j:
            self.sinusbullet_shoot_sound.stop()
            self.shooting_log = False

    def stop_all_move(self):
        self.sinusbullet_shoot_sound.stop()
        self.right_move = False
        self.left_move = False
        self.shooting_log = False


class GoodEnemy(Person):
    def __init__(self, x, y, *group):
        super().__init__(x, y, "Enemys/Enemy_base.png", *group)
        self.t = 0
        self.running_right = []
        for i in range(8):
            self.running_right.append(pygame.transform.scale(load_image("GoodEnemy/Enemy_base_" + str(i) + ".png", -1), (50, 90)))
        self.running_left = []
        for i in range(8):
            x = pygame.transform.scale(load_image("GoodEnemy/Enemy_base_" + str(i) + ".png", -1), (50, 90))
            self.running_left.append(pygame.transform.flip(x, True, False))

    def animate(self):
        if self.oldrunningwasright:
            self.image = self.running_right[self.t]
            self.t += 1
            if self.t > 7:
                self.t = 0
        else:
            self.image = self.running_left[self.t]
            self.t += 1
            if self.t > 7:
                self.t = 0

    def moving(self, floor_sprites, hero_sprites):
        if self_on_screen(self):
            if self.oldrunningwasright:
                if check_block(self.rect.x + 45, self.rect.y + 100, floor_sprites) and\
                        not(check_block(self.rect.x + 45, self.rect.y + 50, floor_sprites)):
                    self.rect.x += 1
                else:
                    self.oldrunningwasright = False
            else:
                if check_block(self.rect.x - 10, self.rect.y + 100, floor_sprites) and\
                        not (check_block(self.rect.x - 10, self.rect.y + 50, floor_sprites)):
                    self.rect.x -= 1
                else:
                    self.oldrunningwasright = True


class BaseEnemy(Person):
    def __init__(self, x, y, *group):
        super().__init__(x, y, "Enemys/Enemy_base.png", *group)
        self.bullet_spawn = 10
        self.t = 0
        self.life = True
        self.running_right = []
        for i in range(8):
            self.running_right.append(
                pygame.transform.scale(load_image("Enemys/Enemy_base_" + str(i) + ".png", -1), (50, 90)))
        self.running_left = []
        for i in range(8):
            x = pygame.transform.scale(load_image("Enemys/Enemy_base_" + str(i) + ".png", -1), (50, 90))
            self.running_left.append(pygame.transform.flip(x, True, False))
        self.Exp_right = []
        for i in range(8):
            self.Exp_right.append(
                pygame.transform.scale(load_image("Enemys/Enemy_Exp_base_" + str(i) + ".png", -1), (50, 90)))
        self.Exp_left = []
        for i in range(8):
            x = pygame.transform.scale(load_image("Enemys/Enemy_Exp_base_" + str(i) + ".png", -1), (50, 90))
            self.Exp_left.append(pygame.transform.flip(x, True, False))

    def animate(self):
        if self.life:
            if self.oldrunningwasright:
                self.image = self.running_right[self.t]
                self.t += 1
                if self.t > 7:
                    self.t = 0
            else:
                self.image = self.running_left[self.t]
                self.t += 1
                if self.t > 7:
                    self.t = 0
        else:
            if self.oldrunningwasright:
                if self.t > 7:
                    self.kill()
                else:
                    self.image = self.Exp_right[self.t]
                    self.t += 1
            else:
                if self.t > 7:
                    self.kill()
                else:
                    self.image = self.Exp_left[self.t]
                    self.t += 1

    def get_hit(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            if self.life:
                self.t = 0
            self.life = False

    def moving(self, floor_sprites, hero_sprites):
        if self_on_screen(self) and self.life:
            if self.oldrunningwasright:
                if check_hero(self.rect.x + 50, self.rect.y + 10, True, hero_sprites):
                    if self.bullet_spawn > 50:
                        self.bullet_spawn = 0
                        return Bullet(self.rect.x + 50, self.rect.y + 25, True, 2, "bull_0.png")
                    else:
                        self.bullet_spawn += 1
                else:
                    self.bullet_spawn = 50
                    if check_block(self.rect.x + 50, self.rect.y + 50, floor_sprites) or \
                            not check_block(self.rect.x + 50, self.rect.y + 100, floor_sprites):
                        self.oldrunningwasright = False
                    self.rect.x += 1
            else:
                if check_hero(self.rect.x - 25, self.rect.y + 10, False, hero_sprites):
                    if self.bullet_spawn > 50:
                        self.bullet_spawn = 0
                        return Bullet(self.rect.x - 25, self.rect.y + 25, False, 2, "bull_0.png")
                    else:
                        self.bullet_spawn += 1
                else:
                    self.bullet_spawn = 50
                    if (check_block(self.rect.x - 5, self.rect.y + 50, floor_sprites)) or \
                            not check_block(self.rect.x - 5, self.rect.y + 100, floor_sprites):
                        self.oldrunningwasright = True
                    self.rect.x -= 1
            return None


class UpEnemy(Person):
    def __init__(self, x, y, *group):
        super().__init__(x, y, "Enemys/Enemy_up_0.png", *group)
        self.bullet_spawn = 1000
        self.herowas = False
        self.t = 0
        self.animations = []
        for i in range(4):
            self.animations.append(load_image("Enemys/Enemy_up_" + str(i) + ".png", -1))

    def animate(self):
        pass

    def moving(self, floor_sprites, hero_sprites):
        if self_on_screen(self):
            if check_hero_down(self.rect.x + 25, self.rect.y + 30, hero_sprites):
                if self.bullet_spawn > 50:
                    self.bullet_spawn = 0
                    self.herowas = True
                else:
                    self.bullet_spawn += 1
            else:
                self.bullet_spawn = 50
            if self.herowas:
                self.image = self.animations[self.t // 5]
                self.t += 1
                if self.t >= 20:
                    self.t = 0
                    self.image = self.animations[self.t // 5]
                    self.herowas = False
                    return DownBullet(self.rect.x + 5, self.rect.y + 30, 5)
            return None


class Saw(pygame.sprite.Sprite):
    def __init__(self, x, y, *group):
        super().__init__(*group)
        self.images = [load_image("Bullets/saw_0.png", -1), load_image("Bullets/saw_1.png", -1),
                       load_image("Bullets/saw_2.png", -1), load_image("Bullets/saw_3.png", -1),
                       load_image("Bullets/saw_4.png", -1), load_image("Bullets/saw_5.png", -1)]
        self.image = self.images[0]
        self.t = 0
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.oldrunningwasright = True
        self.wasDamage = False

        self.beginsound = True
        self.saw_sound = pygame.mixer.Sound("data/Sounds/saw.ogg")
        self.saw_sound.set_volume(0.1)

    def animate(self):
        self.image = self.images[self.t]
        self.t += 1
        if self.t > 5:
            self.t = 0

    def moving(self, floor_sprites, hero_sprites):
        if self_on_screen(self):
            if self.beginsound:
                self.saw_sound.play(-1)
                self.beginsound = False
        else:
            self.beginsound = True
            self.saw_sound.stop()

        if self.oldrunningwasright:
            if check_block(self.rect.x + 70, self.rect.y + 50, floor_sprites) and \
                    not (check_block(self.rect.x + 70, self.rect.y + 15, floor_sprites)):
                self.rect.x += 10
            else:
                self.oldrunningwasright = False
        else:
            if check_block(self.rect.x - 10, self.rect.y + 50, floor_sprites) and \
                    not (check_block(self.rect.x - 10, self.rect.y + 15, floor_sprites)):
                self.rect.x -= 10
            else:
                self.oldrunningwasright = True

        x = pygame.sprite.spritecollideany(self, hero_sprites)
        if x:
            if type(x) == Hero:
                if self.wasDamage:
                    self.wasDamage = False
                    x.get_hit(20)
                    return x
        else:
            self.wasDamage = True


class Boss(Person):
    def __init__(self, *group):
        self.circspos = [(100, 50), (180, 175), (250, 100), (140, 25), (50, 170)]
        self.oldx = 400
        self.oldy = 50
        super().__init__(self.oldx, self.oldy, "Boss/Boss_0.png", *group)
        self.hp = 1000
        self.LeftUpbullet_spawn = 50
        self.LeftDownbullet_spawn = 50
        self.RightUpbullet_spawn = 50
        self.RightDownbullet_spawn = 50
        self.DownLeftbullet_spawn = 50
        self.DownCentbullet_spawn = 50
        self.DownRightbullet_spawn = 50
        self.move = "y+"
        self.t = 0
        self.r = 10
        self.life = True
        self.animations = []
        for i in range(6):
            self.animations.append(load_image("Boss/boss_" + str(i) + ".png", -1))
        self.boss_sound = pygame.mixer.Sound("data/Sounds/boss.ogg")
        self.boss_sound.set_volume(0.5)
        self.mustexp = True

    def explosion(self, screen):
        if self.mustexp:
            self.t += 1
            if self.t % 50 == 0:
                self.boss_sound.play()
        if 10 < self.t <= 50:
            self.r += 1
            pygame.draw.circle(screen, (250, 250, 0), (self.rect.x + self.circspos[0][0], self.rect.y + self.circspos[0][1]), self.r)
            pygame.draw.circle(screen, (255, 255, 255), (self.rect.x + self.circspos[0][0], self.rect.y + self.circspos[0][1]), self.r - 10)
        elif 50 < self.t <= 100:
            self.r += 1
            pygame.draw.circle(screen, (250, 250, 0), (self.rect.x + self.circspos[1][0], self.rect.y + self.circspos[1][1]), self.r)
            pygame.draw.circle(screen, (255, 255, 255), (self.rect.x + self.circspos[1][0], self.rect.y + self.circspos[1][1]), self.r - 10)
        elif 100 < self.t <= 150:
            self.r += 1
            pygame.draw.circle(screen, (250, 250, 0), (self.rect.x + self.circspos[2][0], self.rect.y + self.circspos[2][1]), self.r)
            pygame.draw.circle(screen, (255, 255, 255), (self.rect.x + self.circspos[2][0], self.rect.y + self.circspos[2][1]), self.r - 10)
        elif 150 < self.t <= 200:
            self.r += 1
            pygame.draw.circle(screen, (250, 250, 0), (self.rect.x + self.circspos[3][0], self.rect.y + self.circspos[3][1]), self.r)
            pygame.draw.circle(screen, (255, 255, 255), (self.rect.x + self.circspos[3][0], self.rect.y + self.circspos[3][1]), self.r - 10)
        elif 200 < self.t <= 250:
            self.r += 1
            pygame.draw.circle(screen, (250, 250, 0), (self.rect.x + self.circspos[4][0], self.rect.y + self.circspos[4][1]), self.r)
            pygame.draw.circle(screen, (255, 255, 255), (self.rect.x + self.circspos[4][0], self.rect.y + self.circspos[4][1]), self.r - 10)
        elif self.t > 250:
            self.mustexp = False
            saving_plot(7)
            self.kill()
        if self.r >= 50:
            self.r = 10

    def animate(self):
        if self.life:
            self.image = self.animations[self.t]
            self.t += 1
            if self.t > 5:
                self.t = 0

    def get_hit(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            if self.life:
                self.t = 0
            self.life = False

    def moving(self, floor_sprites, hero_sprites):
        if self.life:
            if check_hero(self.rect.x - 10, self.rect.y + 40, False, hero_sprites):
                if self.LeftUpbullet_spawn > 50:
                    self.LeftUpbullet_spawn = 0
                    return Bullet(self.rect.x - 20, self.rect.y + 30, False, 2, "bull_0.png")
                else:
                    self.LeftUpbullet_spawn += 1
            elif check_hero(self.rect.x - 10, self.rect.y + 110, False, hero_sprites):
                if self.LeftDownbullet_spawn > 50:
                    self.LeftDownbullet_spawn = 0
                    return Bullet(self.rect.x - 20, self.rect.y + 100, False, 2, "bull_0.png")
                else:
                    self.LeftDownbullet_spawn += 1
            elif check_hero(self.rect.x + 310, self.rect.y + 40, True, hero_sprites):
                if self.RightUpbullet_spawn > 50:
                    self.RightUpbullet_spawn = 0
                    return Bullet(self.rect.x + 310, self.rect.y + 35, True, 2, "bull_0.png")
                else:
                    self.RightUpbullet_spawn += 1
            elif check_hero(self.rect.x + 290, self.rect.y + 80, True, hero_sprites):
                if self.RightDownbullet_spawn > 50:
                    self.RightDownbullet_spawn = 0
                    return Bullet(self.rect.x + 310, self.rect.y + 85, True, 2, "bull_0.png")
                else:
                    self.RightDownbullet_spawn += 1
            elif check_hero_down(self.rect.x + 45, self.rect.y + 200, hero_sprites):
                if self.DownLeftbullet_spawn > 50:
                    self.DownLeftbullet_spawn = 0
                    return DownBullet(self.rect.x + 25, self.rect.y + 205, 5)
                else:
                    self.DownLeftbullet_spawn += 1
            elif check_hero_down(self.rect.x + 150, self.rect.y + 180, hero_sprites):
                if self.DownCentbullet_spawn > 50:
                    self.DownCentbullet_spawn = 0
                    return DownBullet(self.rect.x + 130, self.rect.y + 205, 5)
                else:
                    self.DownCentbullet_spawn += 1
            elif check_hero_down(self.rect.x + 250, self.rect.y + 150, hero_sprites):
                if self.DownRightbullet_spawn > 50:
                    self.DownRightbullet_spawn = 0
                    return DownBullet(self.rect.x + 230, self.rect.y + 205, 5)
                else:
                    self.DownRightbullet_spawn += 1
            else:
                self.LeftUpbullet_spawn = 50
                self.LeftDownbullet_spawn = 50
                self.RightUpbullet_spawn = 50
                self.RightDownbullet_spawn = 50
                self.DownLeftbullet_spawn = 50
                self.DownCentbullet_spawn = 50
                self.DownRightbullet_spawn = 50
            if self.move == "y+":
                self.rect.y += 1
                if self.rect.y >= self.oldy + 200:
                    self.move = "x+"
            elif self.move == "x+":
                self.rect.x += 1
                if self.rect.x >= self.oldx + 100:
                    self.move = "y-"
            elif self.move == "y-":
                self.rect.y -= 1
                if self.rect.y <= self.oldy:
                    self.move = "x-"
            elif self.move == "x-":
                self.rect.x -= 1
                if self.rect.x <= self.oldx:
                    self.move = "y+"
