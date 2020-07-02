import socket
import pygame
import json
from io import StringIO
from paddle import Paddle
from ball import Ball
from player import Player

client_a = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_a.bind((socket.gethostname(), 1234))
client_a.setblocking(False)
print(f"Connection from client A has been established.")

pygame.init()
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
# Open a new window
size = (700, 700)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Pong")
paddleA = Paddle(RED, 10, 700)
paddleA.rect.x = 10
paddleA.rect.y = 300
paddleB = Paddle(GREEN, 10, 700)
paddleB.rect.x = 680
paddleB.rect.y = 300
paddleC = Paddle(BLUE, 700, 10)
paddleC.rect.x = 300
paddleC.rect.y = 10
paddleD = Paddle(WHITE, 700, 10)
paddleD.rect.x = 300
paddleD.rect.y = 680

playerA = Player(RED, paddleA)
playerB = Player(GREEN, paddleB)
playerC = Player(BLUE, paddleC)
playerD = Player(WHITE, paddleD)

ball2 = Ball(WHITE, 10, 10)
ball2.rect.x = 345
ball2.rect.y = 195
# This will be a list that will contain all the sprites we intend to use in our game.
all_sprites_list = pygame.sprite.Group()
# Add the car to the list of objects
all_sprites_list.add(paddleA)
all_sprites_list.add(paddleB)
all_sprites_list.add(paddleC)
all_sprites_list.add(paddleD)
balls = []
for index in range(2):
    ball = Ball(WHITE, 10, 10)
    ball.rect.x = 345
    ball.rect.y = 195
    all_sprites_list.add(ball)
    balls.append(ball)
# The loop will carry on until the user exit the game (e.g. clicks the close button).
carryOn = True
# The clock will be used to control how fast the screen updates
clock = pygame.time.Clock()


def check_ball_position(ball_to_be_checked):
    if ball_to_be_checked.rect.x >= 690:
        count_score(ball_to_be_checked, [playerA, playerC, playerD])
        ball_to_be_checked.velocity[0] = -ball_to_be_checked.velocity[0]
    if ball_to_be_checked.rect.x <= 0:
        count_score(ball_to_be_checked, [playerB, playerC, playerD])
        ball_to_be_checked.velocity[0] = -ball_to_be_checked.velocity[0]
    if ball_to_be_checked.rect.y > 690:
        count_score(ball_to_be_checked, [playerA, playerB, playerC])
        ball_to_be_checked.velocity[1] = -ball_to_be_checked.velocity[1]
    if ball_to_be_checked.rect.y < 0:
        count_score(ball_to_be_checked, [playerA, playerB, playerD])
        ball_to_be_checked.velocity[1] = -ball_to_be_checked.velocity[1]

    check_collision_and_set(ball_to_be_checked, playerA)
    check_collision_and_set(ball_to_be_checked, playerB)
    check_collision_and_set(ball_to_be_checked, playerC)
    check_collision_and_set(ball_to_be_checked, playerD)


def check_collision_and_set(ball_to_be_checked, player):
    if pygame.sprite.collide_mask(ball_to_be_checked, player.paddle):
        ball_to_be_checked.lastPlayer = player
        ball_to_be_checked.image.fill(player.color)
        ball_to_be_checked.bounce()


def count_score(current_ball, players):
    for player in players:
        if current_ball.lastPlayer == player:
            player.score += 1


# -------- Main Program Loop -----------
while carryOn:
    # --- Main event loop
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            carryOn = False  # Flag that we are done so we exit this loop
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:  # Pressing the x Key will quit the game
                carryOn = False
    try:
        #print('-------------------------')
        jsonMsg, address = client_a.recvfrom(1024)
        msgaKey = json.load(StringIO(jsonMsg.decode("utf-8")))
        print(jsonMsg.decode("utf-8"))
        print(address)
        if "w" in msgaKey['key']:
            paddleA.moveUp(5)
        if "s" in msgaKey['key']:
            paddleA.moveDown(5)
    except:
        pass

    # --- Game logic should go here
    all_sprites_list.update()
    # Check if the ball is bouncing against any of the 4 walls:
    for ball in balls:
        check_ball_position(ball)
    # --- Drawing code should go here
    # First, clear the screen to black.
    screen.fill(BLACK)
    # Draw the net
    pygame.draw.line(screen, WHITE, [349, 0], [349, 700], 5)
    pygame.draw.line(screen, WHITE, [0, 349], [700, 349], 5)
    # Now let's draw all the sprites in one go. (For now we only have 2 sprites!)
    all_sprites_list.draw(screen)
    # Display scores:
    font = pygame.font.Font(None, 74)
    text = font.render("Hit: " + str(playerA.score), 1, WHITE)
    screen.blit(text, (150, 280))
    text = font.render("Hit: " + str(playerB.score), 1, WHITE)
    screen.blit(text, (420, 280))
    text = font.render("Hit: " + str(playerC.score), 1, WHITE)
    screen.blit(text, (300, 100))
    text = font.render("Hit: " + str(playerD.score), 1, WHITE)
    screen.blit(text, (300, 550))
    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
    # --- Limit to 60 frames per second
    clock.tick(60)
# Once we have exited the main program loop we can stop the game engine:
pygame.quit()
