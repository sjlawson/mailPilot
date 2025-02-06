import random
from pygame import sprite, image


class Island(sprite.Sprite):
    def __init__(self, screen):
        sprite.Sprite.__init__(self)
        self.screen = screen
        self.image = image.load("images/island.gif")
        self.rect = self.image.get_rect()
        self.reset()
        self.dy = 5

    def update(self):
        self.rect.centery += self.dy
        if self.rect.top > self.screen.get_height():
            self.reset()

    def reset(self):
        self.rect.top = 0
        self.rect.centerx = random.randrange(0, self.screen.get_width())
