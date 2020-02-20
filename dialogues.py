import pygame

from functions import check_plot, click_wait, saving_plot, saving_guns


def dialog_with_AGT(self, screen, x):
    pygame.mouse.set_visible(True)
    if check_plot() == 0:
        self.dialog_sprites.draw(screen)
        screen.blit(self.dialog_namefont.render(x[12:], 1, (0, 0, 0)), (115, 370))
        screen.blit(self.dialog_font.render("Рад приветствовать вас, Робот-Наёмник РН-42. Как вам", 1, (0, 0, 0)), (110, 430))
        screen.blit(self.dialog_font.render("уже известно, во время раскопок в нашей шахте было", 1, (0, 0, 0)), (110, 455))
        screen.blit(self.dialog_font.render("обнаружено агрессивно-настроенное существо, которое каким-то образом", 1, (0, 0, 0)), (110, 480))
        screen.blit(self.dialog_font.render("смогло захватить некоторую нашу шахтёрскую технику.", 1, (0, 0, 0)), (110, 505))
        pygame.display.flip()
        click_wait()

        self.dialog_sprites.draw(screen)
        screen.blit(self.dialog_namefont.render(x[12:], 1, (0, 0, 0)), (115, 370))
        screen.blit(self.dialog_font.render("Из незаражённых остались только я, ИЛД1v108,", 1, (0, 0, 0)), (110, 430))
        screen.blit(self.dialog_font.render("ПЛН0105, РСЛ1v410 и погрузчик Джони.", 1, (0, 0, 0)), (110, 455))
        screen.blit(self.dialog_font.render("Бедолага совсем закрылся в себе и ходит целый день кругами.", 1, (0, 0, 0)), (110, 480))
        screen.blit(self.dialog_font.render("Кстати местные погрузчики вооружены, будь на чеку.", 1, (0, 0, 0)), (110, 505))
        pygame.display.flip()
        click_wait()

        self.dialog_sprites.draw(screen)
        screen.blit(self.dialog_namefont.render(x[12:], 1, (0, 0, 0)), (115, 370))
        screen.blit(self.dialog_font.render("Чем дольше работа в шахте стоит, тем дольше страна", 1, (0, 0, 0)), (110, 430))
        screen.blit(self.dialog_font.render("остаётся без поставок медной руды. Сначала вам", 1, (0, 0, 0)), (110, 455))
        screen.blit(self.dialog_font.render("необходимо освободить моих коллег из плена этого существа.", 1, (0, 0, 0)), (110, 480))
        screen.blit(self.dialog_font.render("Первый - ИЛД1v108. Он прячется в Мат. офисе на третьем уровне.", 1, (0, 0, 0)), (110, 505))
        pygame.display.flip()
        click_wait()

        self.dialog_sprites.draw(screen)
        screen.blit(self.dialog_namefont.render(x[12:], 1, (0, 0, 0)), (115, 370))
        screen.blit(self.dialog_font.render("Думаю, вы с лёгкостью сломаете ящики, которыми", 1, (0, 0, 0)), (110, 430))
        screen.blit(self.dialog_font.render("я забарикадировал своих товарищей в ловушке с", 1, (0, 0, 0)), (110, 455))
        screen.blit(self.dialog_font.render("захваченной техникой. Само собой, я сделал это ради", 1, (0, 0, 0)), (110, 480))
        screen.blit(self.dialog_font.render("общей безопасности.", 1, (0, 0, 0)), (110, 505))
        pygame.display.flip()
        click_wait()
    elif check_plot() == 1:
        self.dialog_sprites.draw(screen)
        screen.blit(self.dialog_namefont.render(x[12:], 1, (0, 0, 0)), (115, 370))
        screen.blit(self.dialog_font.render("Похоже у ИЛД1v108 есть что-то для тебя", 1, (0, 0, 0)), (110, 430))
        pygame.display.flip()
        click_wait()
    elif check_plot() == 2:
        self.dialog_sprites.draw(screen)
        screen.blit(self.dialog_namefont.render(x[12:], 1, (0, 0, 0)), (115, 370))
        screen.blit(self.dialog_font.render("Похоже что СИНУС-ПУШКА компенсирует", 1, (0, 0, 0)), (110, 430))
        screen.blit(self.dialog_font.render("тебе отсутствие коленей. Теперь ты сможешь", 1, (0, 0, 0)), (110, 455))
        screen.blit(self.dialog_font.render("попасть в Мед. офис, в котором прячется ПЛН0v105", 1, (0, 0, 0)), (110, 480))
        screen.blit(self.dialog_font.render("Спасёшь его и, может, получишь что-то новое.", 1, (0, 0, 0)), (110, 505))
        pygame.display.flip()
        click_wait()
    elif check_plot() == 3:
        self.dialog_sprites.draw(screen)
        screen.blit(self.dialog_namefont.render(x[12:], 1, (0, 0, 0)), (115, 370))
        screen.blit(self.dialog_font.render("Ты очень нам помогаешь, спасибо.", 1, (0, 0, 0)), (110, 430))
        screen.blit(self.dialog_font.render("ПЛН0v105 сказал что хочет тебе что-то отдать.", 1, (0, 0, 0)), (110, 455))
        pygame.display.flip()
        click_wait()
    elif check_plot() == 4:
        self.dialog_sprites.draw(screen)
        screen.blit(self.dialog_namefont.render(x[12:], 1, (0, 0, 0)), (115, 370))
        screen.blit(self.dialog_font.render("ГОЛОВОКРАБ поможет тебе попасть в Муз. подвал", 1, (0, 0, 0)), (110, 430))
        screen.blit(self.dialog_font.render("Там ты найдёшь РСЛ1v410.", 1, (0, 0, 0)), (110, 455))
        pygame.display.flip()
        click_wait()
    elif check_plot() == 5:
        self.dialog_sprites.draw(screen)
        screen.blit(self.dialog_namefont.render(x[12:], 1, (0, 0, 0)), (115, 370))
        screen.blit(self.dialog_font.render("У РСЛ1v410 новая пушка для тебя.", 1, (0, 0, 0)), (110, 430))
        pygame.display.flip()
        click_wait()
    elif check_plot() == 6:
        self.dialog_sprites.draw(screen)
        screen.blit(self.dialog_namefont.render(x[12:], 1, (0, 0, 0)), (115, 370))
        screen.blit(self.dialog_font.render("Если музыкальная пушка это источник звуковых волн,", 1, (0, 0, 0)), (110, 430))
        screen.blit(self.dialog_font.render("то ты сможешь разбить ей стекло, которым завалена", 1, (0, 0, 0)), (110, 455))
        screen.blit(self.dialog_font.render("шахта. Сможешь ли ты уничтожить существо? Или у тебя есть другой", 1, (0, 0, 0)), (110, 480))
        screen.blit(self.dialog_font.render("вариант?", 1, (0, 0, 0)), (110, 505))
        pygame.display.flip()
        click_wait()
        self.dialog_sprites.draw(screen)
        screen.blit(self.dialog_namefont.render(x[12:], 1, (0, 0, 0)), (115, 370))
        screen.blit(self.dialog_font.render("Шучу, другого варианта нет.", 1, (0, 0, 0)), (110, 430))
        screen.blit(self.dialog_font.render("Просто уничтожь его и возвращайся туда, откуда пришёл.", 1, (0, 0, 0)), (110, 480))
        pygame.display.flip()
        click_wait()
    pygame.mouse.set_visible(False)


def dialog_with_ILD(self, screen, x):
    pygame.mouse.set_visible(True)
    if check_plot() == 0:
        self.dialog_sprites.draw(screen)
        screen.blit(self.dialog_namefont.render(x[12:], 1, (0, 0, 0)), (115, 370))
        screen.blit(self.dialog_font.render("Рад приветствовать вас, Робот-Наёмник РН-42.", 1, (0, 0, 0)),
                    (110, 430))
        screen.blit(self.dialog_font.render("Скорее возвращаемcя на главную площадь!", 1, (0, 0, 0)),
                    (110, 455))
        pygame.display.flip()
        saving_plot(1)
        click_wait()
        return "level_1"
    elif check_plot() == 1:
        self.dialog_sprites.draw(screen)
        self.newgun_sprites.draw(screen)
        screen.blit(self.dialog_gunfont.render("СИНУС-ПУШКА", 1, (255, 255, 255)), (325, 150))
        screen.blit(self.dialog_namefont.render(x[12:], 1, (0, 0, 0)), (115, 370))
        screen.blit(self.dialog_font.render("Спасибо, что спас меня. Знаешь, пока я был", 1, (0, 0, 0)),
                    (110, 430))
        screen.blit(self.dialog_font.render("в Мат. офисе я разработал новый вид оружия", 1, (0, 0, 0)),
                    (110, 455))
        screen.blit(self.dialog_font.render("Я назвал его СИНУС-ПУШКА (tm). В знак моей благодарности за", 1, (0, 0, 0)), (110, 480))
        screen.blit(self.dialog_font.render("спасение, ты можешь взять тестовый образец.", 1, (0, 0, 0)), (110, 505))
        saving_guns(1)
        saving_plot(2)
        pygame.display.flip()
        click_wait()
    elif check_plot() == 2:
        self.dialog_sprites.draw(screen)
        screen.blit(self.dialog_namefont.render(x[12:], 1, (0, 0, 0)), (115, 370))
        screen.blit(self.dialog_font.render("Спаси ПЛН0v105!", 1, (0, 0, 0)),
                    (110, 430))
        pygame.display.flip()
        click_wait()
    elif check_plot() == 3:
        self.dialog_sprites.draw(screen)
        screen.blit(self.dialog_namefont.render(x[12:], 1, (0, 0, 0)), (115, 370))
        screen.blit(self.dialog_font.render("Ты спас ПЛН0v105!", 1, (0, 0, 0)), (110, 430))
        screen.blit(self.dialog_font.render("Похоже у него что-то есть для тебя.", 1, (0, 0, 0)), (110, 455))
        pygame.display.flip()
        click_wait()
    elif check_plot() == 4:
        self.dialog_sprites.draw(screen)
        screen.blit(self.dialog_namefont.render(x[12:], 1, (0, 0, 0)), (115, 370))
        screen.blit(self.dialog_font.render("Остался только РСЛ1v410.", 1, (0, 0, 0)), (110, 430))
        pygame.display.flip()
        click_wait()
    elif check_plot() == 5:
        self.dialog_sprites.draw(screen)
        screen.blit(self.dialog_namefont.render(x[12:], 1, (0, 0, 0)), (115, 370))
        screen.blit(self.dialog_font.render("РСЛ1v410 вернулся!", 1, (0, 0, 0)), (110, 430))
        pygame.display.flip()
        click_wait()
    elif check_plot() == 6:
        self.dialog_sprites.draw(screen)
        screen.blit(self.dialog_namefont.render(x[12:], 1, (0, 0, 0)), (115, 370))
        screen.blit(self.dialog_font.render("Музыкальная пушка? Звучит как плагиат.", 1, (0, 0, 0)), (110, 430))
        pygame.display.flip()
        click_wait()
    pygame.mouse.set_visible(False)


def dialog_with_PLN(self, screen, x):
    pygame.mouse.set_visible(True)
    if check_plot() == 2:
        self.dialog_sprites.draw(screen)
        screen.blit(self.dialog_namefont.render(x[12:], 1, (0, 0, 0)), (115, 370))
        screen.blit(self.dialog_font.render("Рад приветствовать вас, Робот-Наёмник РН-42.", 1, (0, 0, 0)), (110, 430))
        screen.blit(self.dialog_font.render("Спасибо, что спасаешь меня.", 1, (0, 0, 0)), (110, 455))
        screen.blit(self.dialog_font.render("Скорее, возвращаемся на площадь!", 1, (0, 0, 0)), (110, 480))
        pygame.display.flip()
        saving_plot(3)
        click_wait()
        return "level_1"
    elif check_plot() == 3:
        self.dialog_sprites.draw(screen)
        self.newgun_sprites.draw(screen)
        screen.blit(self.dialog_gunfont.render("ГОЛОВОКРАБ", 1, (255, 255, 255)), (350, 150))
        screen.blit(self.dialog_namefont.render(x[12:], 1, (0, 0, 0)), (115, 370))
        screen.blit(self.dialog_font.render("Ещё раз спасибо за спасение.", 1, (0, 0, 0)), (110, 430))
        screen.blit(self.dialog_font.render("Пока я был в Мед. офисе я осмотрел заражённых.", 1, (0, 0, 0)), (110, 455))
        screen.blit(self.dialog_font.render("Как их освободить я не выяснил, однако я собрал новую", 1, (0, 0, 0)), (110, 480))
        screen.blit(self.dialog_font.render("пушку. Возьми ГОЛОВОКРАБ и уничтожай своих врагов!", 1, (0, 0, 0)), (110, 505))
        pygame.display.flip()
        saving_plot(4)
        saving_guns(2)
        click_wait()
    elif check_plot() == 4:
        self.dialog_sprites.draw(screen)
        screen.blit(self.dialog_namefont.render(x[12:], 1, (0, 0, 0)), (115, 370))
        screen.blit(self.dialog_font.render("Разберись уже с РСЛ1v410!", 1, (0, 0, 0)), (110, 430))
        pygame.display.flip()
        click_wait()
    elif check_plot() == 5:
        self.dialog_sprites.draw(screen)
        screen.blit(self.dialog_namefont.render(x[12:], 1, (0, 0, 0)), (115, 370))
        screen.blit(self.dialog_font.render("У РСЛ1v410 что-то звучащее.", 1, (0, 0, 0)), (110, 430))
        pygame.display.flip()
        click_wait()
    elif check_plot() == 6:
        self.dialog_sprites.draw(screen)
        screen.blit(self.dialog_namefont.render(x[12:], 1, (0, 0, 0)), (115, 370))
        screen.blit(self.dialog_font.render("Отомсти за тех, кто сошёл с тобой с одного конвейера!", 1, (0, 0, 0)), (110, 430))
        pygame.display.flip()
        click_wait()
    pygame.mouse.set_visible(False)


def dialog_with_RSL(self, screen, x):
    pygame.mouse.set_visible(True)
    if check_plot() == 4:
        self.dialog_sprites.draw(screen)
        screen.blit(self.dialog_namefont.render(x[12:], 1, (0, 0, 0)), (115, 370))
        screen.blit(self.dialog_font.render("Я начал думать что меня никто не спасёт...", 1, (0, 0, 0)), (110, 430))
        pygame.display.flip()
        saving_plot(5)
        click_wait()
        return "level_1"
    elif check_plot() == 5:
        self.dialog_sprites.draw(screen)
        self.newgun_sprites.draw(screen)
        screen.blit(self.dialog_gunfont.render("Музыкальная пушка", 1, (255, 255, 255)), (325, 150))
        screen.blit(self.dialog_namefont.render(x[12:], 1, (0, 0, 0)), (115, 370))
        screen.blit(self.dialog_font.render("Спасибо за спасение, РН-42.", 1, (0, 0, 0)), (110, 430))
        screen.blit(self.dialog_font.render("Знаешь, в плену мне было чем заняться.", 1, (0, 0, 0)), (110, 455))
        screen.blit(self.dialog_font.render("Я разработал классную музыкальную пушку...", 1, (0, 0, 0)), (110, 480))
        pygame.display.flip()
        saving_guns(3)
        saving_plot(6)
        click_wait()
        self.dialog_sprites.draw(screen)
        screen.blit(self.dialog_namefont.render(x[12:], 1, (0, 0, 0)), (115, 370))
        screen.blit(self.dialog_font.render("...И загрузил в неё всего один трек.", 1, (0, 0, 0)), (110, 430))
        screen.blit(self.dialog_font.render("Кусочек ремикса одной старой песни.", 1, (0, 0, 0)), (110, 455))
        screen.blit(self.dialog_font.render("Надеюсь тебе не надоест.", 1, (0, 0, 0)), (110, 480))
        pygame.display.flip()
        click_wait()
    elif check_plot() == 6:
        self.dialog_sprites.draw(screen)
        screen.blit(self.dialog_namefont.render(x[12:], 1, (0, 0, 0)), (115, 370))
        screen.blit(self.dialog_font.render("Ну всё, тебе осталось только выйти на битву с боссом.", 1, (0, 0, 0)), (110, 430))
        pygame.display.flip()
        click_wait()
    pygame.mouse.set_visible(False)
