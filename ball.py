import pygame
from random import randint

BLACK = (0, 0, 0)


class Ball(pygame.sprite.Sprite):
    # This class represents a car. It derives from the "Sprite" class in Pygame.

    def __init__(self, color, width, height):
        # Call the parent class (Sprite) constructor
        super().__init__()

        self.lastPlayer = None

        # Pass in the color of the car, and its x and y position, width and height.
        # Set the background color and set it to be transparent
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        self.mask = pygame.Mask([width, height], True)

        # Draw the ball (a rectangle!)
        pygame.draw.rect(self.image, color, [0, 0, width, height])

        self.velocity = [randint(-8, 8), randint(-8, 8)]

        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()

    def color(self, color):
        self.image.fill(color)

    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

    def bounce(self):
        if self.rect.x <= 40:
            self.velocity[0] = randint(1, 8)
        elif self.rect.x >= 680:
            self.velocity[0] = randint(-8, -1)

        if self.rect.y <= 40:
            self.velocity[1] = randint(1, 8)
        elif self.rect.y >= 680:
            self.velocity[1] = randint(-8, -1)
