from tkinter import Tk, Label, Canvas
from snake import Snake
from food import Food
from poison import Poison
from const import GAME_WIDTH, GAME_HEIGHT, BACKGROUND_COLOR, INITIAL_SPEED, SPACE_SIZE

class Main:
    def __init__(self):
        self.window = Tk()
        self.window.title("Snake Game")
        self.window.resizable(False, False)
        
        self.direction = 'down'
        self.score = 0
        self.poison_collision_count = 0
        self.speed = INITIAL_SPEED

        # Setup UI elements
        self.label = Label(self.window, text="Score: {}".format(self.score), font=('consolas', 40))
        self.label.pack()

        self.canvas = Canvas(self.window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
        self.canvas.pack()

        # Center window
        self.window.update()
        window_width = self.window.winfo_width()
        window_height = self.window.winfo_height()
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))
        self.window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Bind keys
        self.window.bind('<Left>', lambda event: self.change_direction('left'))
        self.window.bind('<Right>', lambda event: self.change_direction('right'))
        self.window.bind('<Up>', lambda event: self.change_direction('up'))
        self.window.bind('<Down>', lambda event: self.change_direction('down'))

        # Initialize game components
        self.snake = Snake(self.canvas)
        self.food = Food(self.canvas)
        self.poison = None

        # Start game
        self.next_turn()

        self.window.mainloop()

    def next_turn(self):
        x, y = self.snake.coordinates[0]

        # Movement logic
        if self.direction == "up":
            y -= SPACE_SIZE
        elif self.direction == "down":
            y += SPACE_SIZE
        elif self.direction == "right":
            x += SPACE_SIZE
        elif self.direction == "left":
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

        # Move snake head
        self.snake.coordinates.insert(0, [x, y])
        square = self.canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill="#008000")
        self.snake.squares.insert(0, square)

        # Check food collision
        if x == self.food.coordinates[0] and y == self.food.coordinates[1]:
            self.score += 1
            self.label.config(text="Score: {}".format(self.score))
            self.canvas.delete("food")
            self.food = Food(self.canvas)

            # Generate poison after 10 points
            if self.score >= 10 and self.poison is None:
                self.poison = Poison(self.canvas)

        else:
            del self.snake.coordinates[-1]
            self.canvas.delete(self.snake.squares[-1])
            del self.snake.squares[-1]

        # Poison collision
        if self.poison and x == self.poison.coordinates[0] and y == self.poison.coordinates[1]:
            self.score -= 3
            self.poison_collision_count += 1
            self.label.config(text="Score: {}".format(self.score))

            if self.poison_collision_count >= 3:
                self.game_over()
                return

            self.canvas.delete("poison")
            self.poison = None

        # Check self-collision
        if self.check_collisions():
            self.game_over()
        else:
            self.window.after(self.speed, self.next_turn)

    def change_direction(self, new_direction):
        if new_direction == 'left' and self.direction != 'right':
            self.direction = new_direction
        elif new_direction == 'right' and self.direction != 'left':
            self.direction = new_direction
        elif new_direction == 'up' and self.direction != 'down':
            self.direction = new_direction
        elif new_direction == 'down' and self.direction != 'up':
            self.direction = new_direction

    def check_collisions(self):
        x, y = self.snake.coordinates[0]
        return (x, y) in self.snake.coordinates[1:]

    def game_over(self):
        self.canvas.delete("all")
        self.canvas.create_text(self.canvas.winfo_width() / 2, self.canvas.winfo_height() / 2,
                                font=('consolas', 70), text="GAME OVER", fill="red", tag="gameover")

if __name__ == "__main__":
    Main()
