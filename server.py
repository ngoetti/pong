import socket
import pygame
import json
from io import StringIO
from paddle import Paddle
from ball import Ball
from player import Player

ip = '172.16.17.220'
number_of_balls = 5

client_a = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_a.bind((ip, 1111))
client_a.setblocking(False)
client_b = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_b.bind((ip, 2222))
client_b.setblocking(False)
client_c = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_c.bind((ip, 3333))
client_c.setblocking(False)
client_d = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_d.bind((ip, 4444))
client_d.setblocking(False)

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
paddleA = Paddle(WHITE, 10, 700)
paddleA.rect.x = 10
paddleA.rect.y = 0
paddleB = Paddle(WHITE, 10, 700)
paddleB.rect.x = 680
paddleB.rect.y = 0
paddleC = Paddle(WHITE, 700, 10)
paddleC.rect.x = 0
paddleC.rect.y = 10
paddleD = Paddle(WHITE, 700, 10)
paddleD.rect.x = 0
paddleD.rect.y = 680

playerA = Player(RED, paddleA, True)
playerB = Player(GREEN, paddleB, True)
playerC = Player(BLUE, paddleC, False)
playerD = Player(WHITE, paddleD, False)

# This will be a list that will contain all the sprites we intend to use in our game.
all_sprites_list = pygame.sprite.Group()
# Add the car to the list of objects
all_sprites_list.add(paddleA)
all_sprites_list.add(paddleB)
all_sprites_list.add(paddleC)
all_sprites_list.add(paddleD)
balls = []
for index in range(number_of_balls):
    ball = Ball(WHITE, 10, 10)
    ball.rect.x = 350
    ball.rect.y = 350
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
        if player.name is not "":
            ball_to_be_checked.lastPlayer = player
            ball_to_be_checked.image.fill(player.color)
        ball_to_be_checked.bounce()


def count_score(current_ball, players):
    for player in players:
        if current_ball.lastPlayer == player:
            player.score += 1


def paddle_action(client, player, x, y, w, b):
    jsonMsg, address = client.recvfrom(1024)
    msgaKey = json.load(StringIO(jsonMsg.decode("utf-8")))
    print(jsonMsg.decode("utf-8"))
    print(address)
    if 'name' in msgaKey.keys():
        player.name = msgaKey['name']
        player.paddle.changeSize(player.color, w, b)
        player.paddle.rect.y = y
        player.paddle.rect.x = x
        player.score = 0
    elif player.name is not "":
        if player.vertical:
            player.paddle.rect.y = int(msgaKey['position'])
        else:
            player.paddle.rect.x = int(msgaKey['position'])


def find_player_with_max_score(players):
    max_score = max(map(lambda p: p.score, players))
    return next(x for x in players if x.score == max_score)


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
        paddle_action(client_a, playerA, 10, 300, 10, 100)
    except:
        pass
    try:
        paddle_action(client_b, playerB, 680, 300, 10, 100)
    except:
        pass
    try:
        paddle_action(client_c, playerC, 300, 10, 100, 10)
    except:
        pass
    try:
        paddle_action(client_d, playerD, 300, 680, 100, 10)
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
    font = pygame.font.Font(None, 50)
    if max([playerA.score, playerB.score, playerC.score, playerD.score]) >= 20:
        playerWithMaxScore = find_player_with_max_score([playerA, playerB, playerC, playerD])
        text = font.render("Player " + playerWithMaxScore.name + " Won", 1, playerWithMaxScore.color)
        screen.blit(text, (300, 350))
    else:
        text = font.render(playerA.name + ": " + str(playerA.score), 1, playerA.color)
        if playerA.name is not "":
            screen.blit(text, (150, 280))
        text = font.render(playerB.name + ": " + str(playerB.score), 1, playerB.color)
        if playerB.name is not "":
            screen.blit(text, (420, 280))
        text = font.render(playerC.name + ": " + str(playerC.score), 1, playerC.color)
        if playerC.name is not "":
            screen.blit(text, (300, 100))
        text = font.render(playerD.name + ": " + str(playerD.score), 1, playerD.color)
        if playerD.name is not "":
            screen.blit(text, (300, 550))
    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
    # --- Limit to 60 frames per second
    clock.tick(60)
# Once we have exited the main program loop we can stop the game engine:
pygame.quit()
