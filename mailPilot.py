import pygame
import random
import mpPlane

from mpIsland import Island

__author__ = "samuel"
__date__ = "$03-Apr-2011 11:10:22$"


pygame.init()
screen = pygame.display.set_mode((640, 480))


class ScoreBoard(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.lives = 5
        self.score = 0
        self.font = pygame.font.SysFont("None", 50)

    def update(self):
        self.text = "Planes: %d, Score: %d" % (self.lives, self.score)
        self.image = self.font.render(self.text, 1, (255, 255, 0))
        self.rect = self.image.get_rect()


class Ocean(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/ocean.gif")
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.dy = 5
        self.reset()

    def update(self):
        self.rect.bottom += self.dy
        if self.rect.top >= 0:
            self.reset()

    def reset(self):
        self.rect.bottom = screen.get_height()


class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/cloud.gif")
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.reset()

    def update(self):
        self.rect.centerx += self.dx
        self.rect.centery += self.dy
        if self.rect.top > screen.get_height():
            self.reset()

    def reset(self):
        self.rect.bottom = 0
        self.rect.centerx = random.randrange(0, screen.get_width())
        self.dy = random.randrange(2, 10)
        self.dx = random.randrange(-2, 2)


def game():
    # display setup

    pygame.display.set_caption("Mail Pilot!")

    # Entities
    background = pygame.Surface(screen.get_size())
    background.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    scoreboard = ScoreBoard()
    island = Island(screen=screen)
    plane = mpPlane.Plane()
    ocean = Ocean()
    clouds = []
    for i in range(3):
        clouds.append(Cloud())

    friendSprites = pygame.sprite.OrderedUpdates(ocean, island, plane)
    cloudSprites = pygame.sprite.Group(clouds)
    scoreSprite = pygame.sprite.Group(scoreboard)

    # Action - ALTER steps
    # A - assign values to key variables
    clock = pygame.time.Clock()
    keepGoing = True
    # L - loop
    while keepGoing:
        # Timer sets frame rate
        clock.tick(30)

        # Event handling
        pygame.mouse.set_visible(False)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                keepGoing = False
        # check collisions
        if plane.rect.colliderect(island.rect):
            plane.sndYay.play()
            island.reset()
            scoreboard.score += 100

        hitClouds = pygame.sprite.spritecollide(plane, cloudSprites, False)
        if hitClouds:
            plane.sndThunder.play()
            scoreboard.lives -= 1
            if scoreboard.lives <= 0:
                # print "Game over!"
                # scoreboard.lives = 5
                # scoreboard.score = 0
                keepGoing = False
        for theCloud in hitClouds:
            theCloud.reset()

        # - single collision method
        # if plane.rect.colliderect(cloud.rect):
        #    plane.sndThunder.play()
        #    cloud.reset()

        # R - refresh display
        # allSprites.clear(screen, background)
        friendSprites.update()
        cloudSprites.update()
        scoreSprite.update()

        friendSprites.draw(screen)
        cloudSprites.draw(screen)
        scoreSprite.draw(screen)

        pygame.display.flip()

    pygame.mouse.set_visible(True)
    plane.sndEngine.stop()
    return scoreboard.score


def instructions(score):
    plane = mpPlane.Plane()
    ocean = Ocean()

    allSprites = pygame.sprite.OrderedUpdates(ocean, plane)
    insFont = pygame.font.SysFont("None", 40)

    instructions = (
        "Mail Pilot.  Last score: %d" % score,
        "Instructions:  You are a mail pilot,",
        "delivering mail to the islands.",
        "",
        "Fly over an island to drop the mail,",
        "but be careful not to fly too close",
        "to the storm clouds. Your plane will ",
        "fall apart if it is hit by lightning ",
        "too many times.",
        "",
        "Good luck!",
        "",
        "Click the mouse to start, escape to quit..."
    )

    insLabels = []
    for line in instructions:
        tempLabel = insFont.render(line, 1, (255, 255, 0))
        insLabels.append(tempLabel)

    keepGoing = True
    clock = pygame.time.Clock()
    pygame.mouse.set_visible(False)
    while keepGoing:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
                donePlaying = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                keepGoing = False
                donePlaying = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                keepGoing = False
                donePlaying = True

        allSprites.update()
        allSprites.draw(screen)

        for i in range(len(insLabels)):
            screen.blit(insLabels[i], (50, 30*i))

        pygame.display.flip()

    plane.sndEngine.stop()
    pygame.mouse.set_visible(True)
    return donePlaying


def main():
    donePlaying = False
    score = 0
    while not donePlaying:
        donePlaying = instructions(score)
        if not donePlaying:
            score = game()


if __name__ == "__main__":
    main()
