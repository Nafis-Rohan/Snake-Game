from tkinter import Canvas
from const import SPACE_SIZE, SNAKE_COLOR

class Snake:
    def __init__(self, canvas: Canvas):
        self.body_size = 3
        self.coordinates = []
        self.squares = []

        for i in range(0, self.body_size):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)
