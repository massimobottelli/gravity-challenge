import pygame
import math
import random

# Define constants
NAME = "GravityChallenge"
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
WIDTH = 450
HEIGHT = 700
BALL_RADIUS = 10
OFFSET = BALL_RADIUS + 5
NUM_HOLES = 100
MIN_HOLE_SIZE = BALL_RADIUS
MAX_HOLE_SIZE = BALL_RADIUS * 3
ORIGIN_1 = [0, 0]
ORIGIN_2 = [WIDTH, 0]

# Controls
LEFT_SHORTEN = pygame.K_w  # Shorten left cord
LEFT_LENGTHEN = pygame.K_s  # Lengthen left cord
RIGHT_SHORTEN = pygame.K_o  # Shorten right cord
RIGHT_LENGTHEN = pygame.K_k  # Lengthen right cord
LEFT = 0
RIGHT = 1
SHORTEN = -1
LENGTHEN = 1
STEP = 5


def init_game():
    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(NAME)
    return screen


def random_holes(num_holes):
    holes_array = []

    for _ in range(num_holes):
        hole_random_x = random.randint(MAX_HOLE_SIZE, WIDTH - MAX_HOLE_SIZE)
        hole_random_y = random.randint(MAX_HOLE_SIZE, HEIGHT - MAX_HOLE_SIZE * 2)
        hole_radius = random.randint(MIN_HOLE_SIZE, MAX_HOLE_SIZE)

        no_overlap_area_x1 = hole_random_x - hole_radius - OFFSET
        no_overlap_area_y1 = hole_random_y - hole_radius - OFFSET
        no_overlap_area_x2 = hole_radius * 2 + OFFSET
        no_overlap_area_y2 = hole_radius * 2 + OFFSET

        hole = pygame.Rect(no_overlap_area_x1, no_overlap_area_y1, no_overlap_area_x2, no_overlap_area_y2)

        # Check if the new hole overlaps with any existing hole
        if any(hole.colliderect(existing_hole) for existing_hole in holes_array):
            continue

        holes_array.append(hole)

    return holes_array


def draw_holes(holes_array, screen):

    # Draw all the holes
    for hole in holes_array:
        hole_center = (hole.x + hole.width // 2, hole.y + hole.height // 2)
        hole_radius = (hole.width - OFFSET) // 2
        pygame.draw.circle(screen, WHITE, hole_center, hole_radius, 1)


def adjust_cord(cord_id, direction, length):
    # Change the length of the cord
    length[cord_id] += direction * STEP
    return length


def calculate_position(radius1, radius2):
    # Calculate ball position given the length of the two cords
    distance = math.dist(ORIGIN_1, ORIGIN_2)
    angle = math.acos((radius1 ** 2 + distance ** 2 - radius2 ** 2) / (2 * radius1 * distance))
    dx = ORIGIN_2[0] - ORIGIN_1[0]
    dy = ORIGIN_2[1] - ORIGIN_1[1]
    angle1 = math.atan2(dy, dx)
    angle2 = angle1 + angle
    point = (ORIGIN_1[0] + radius1 * math.cos(angle2), ORIGIN_1[1] + radius1 * math.sin(angle2))
    return point


# Main

# Initial cords length
initial_length = math.hypot(WIDTH/2, HEIGHT)
cord_length = [initial_length, initial_length]

# Define random holes
holes = random_holes(NUM_HOLES)

# Initialize board
board = init_game()

running = True
while running:
    event = pygame.event.wait()
    if event.type == pygame.QUIT:
        running = False
    elif event.type == pygame.KEYDOWN:

        if event.key == pygame.K_q:
            # Quit game
            running = False

        elif event.key == LEFT_SHORTEN:
            # Shorten left cord
            cord_length = adjust_cord(LEFT, SHORTEN, cord_length)

        elif event.key == LEFT_LENGTHEN:
            # Lengthen left cord
            cord_length = adjust_cord(LEFT, LENGTHEN, cord_length)

        elif event.key == RIGHT_SHORTEN:
            # Shorten right cord
            cord_length = adjust_cord(RIGHT, SHORTEN, cord_length)

        elif event.key == RIGHT_LENGTHEN:
            # Lengthen right cord
            cord_length = adjust_cord(RIGHT, LENGTHEN, cord_length)

    # Calculate ball position
    ball_pos = calculate_position(cord_length[LEFT], cord_length[RIGHT])

    board.fill(BLACK)

    # Draw random holes on the board
    draw_holes(holes, board)

    # Draw the ball
    pygame.draw.circle(board, WHITE, ball_pos, BALL_RADIUS)

    # Draw the cords
    pygame.draw.line(board, WHITE, ORIGIN_1, (ball_pos[0], ball_pos[1]))
    pygame.draw.line(board, WHITE, ORIGIN_2, (ball_pos[0], ball_pos[1]))

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
