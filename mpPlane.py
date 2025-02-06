import pygame


class Plane(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/plane.gif")
        self.rect = self.image.get_rect()

        if not pygame.mixer:
            print("Problem with sound")
        else:
            pygame.mixer.init()
            self.sndYay = pygame.mixer.Sound("images/yay.ogg")
            self.sndThunder = pygame.mixer.Sound("images/thunder.ogg")
            self.sndEngine = pygame.mixer.Sound("images/engine.ogg")
            self.sndEngine.play(-1)

    def update(self):
        mousex, mousey = pygame.mouse.get_pos()
        self.rect.center = (mousex, 430)
        # self.rect.center = pygame.mouse.get_pos()
