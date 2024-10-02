import random
from tkinter import Canvas
from const import GAME_WIDTH, GAME_HEIGHT, SPACE_SIZE

class Poison:
    def __init__(self, canvas: Canvas):
        x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE

        self.coordinates = [x, y]

        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill="violet", tag="poison")
