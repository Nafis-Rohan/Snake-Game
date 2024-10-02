from snake import Snake
from food import Food
from poison import Poison
from const import SPACE_SIZE, INITIAL_SPEED, GAME_WIDTH, GAME_HEIGHT,SNAKE_COLOR
from tkinter import Canvas

SPEED = INITIAL_SPEED
poison_collision_count = 0
direction = 'down'

def next_turn(snake: Snake, food: Food, canvas: Canvas, label, poison: Poison = None):
    global SPEED, poison_collision_count

    x, y = snake.coordinates[0]

    # Movement logic
    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE

    # Border wrapping
    if x < 0:
        x = GAME_WIDTH - SPACE_SIZE
    elif x >= GAME_WIDTH:
        x = 0
    if y < 0:
        y = GAME_HEIGHT - SPACE_SIZE
    elif y >= GAME_HEIGHT:
        y = 0

    snake.coordinates.insert(0, (x, y))
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
    snake.squares.insert(0, square)

    # Check for collisions with food, poison, and self, then handle the result
    # (Refer to your existing logic for handling food, poison, and self-collisions)
