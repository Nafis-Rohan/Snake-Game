from tkinter import *
import random

# Constants
GAME_WIDTH = 1200
GAME_HEIGHT = 700
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = "#008000"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"
INITIAL_SPEED = 70
SPEED = INITIAL_SPEED  # Speed will be updated during the game

# Snake class
class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []  # track body
        self.squares = []  # visual part of snake

        for i in range(0, BODY_PARTS):  # mainly its generating the snake according to its bodyPart value
            self.coordinates.append([0, 0])  # each time it adds the position from 0,0 

        for x, y in self.coordinates:  # body can go x,y 
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")  # draw a piece of snake 
            self.squares.append(square)  # after drawing the square, it's saved in the squares(list)

# Food class
class Food:
    def __init__(self):
        x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE  # for x-axis
        y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE  # for y-axis

        self.coordinates = [x, y]  # saves the randomly chosen x and y positions

        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")  # draw the food

# next_turn function: Handles the movement of the snake and checks for food collisions
# Poison class
class Poison:
    def __init__(self):
        x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE  # for x-axis
        y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE  # for y-axis

        self.coordinates = [x, y]  # saves the randomly chosen x and y positions

        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill="violet", tag="poison")  # draw the poison

# next_turn function: Updated to handle poison collision
def next_turn(snake, food, poison=None):
    global SPEED, poison_collision_count  # Added poison_collision_count to track collisions

    x, y = snake.coordinates[0]  # taking the head position of the snake and storing it in x, y

    # Movement logic
    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
        
    # Border wrapping logic
    if x < 0:
        x = GAME_WIDTH - SPACE_SIZE
    elif x >= GAME_WIDTH:
        x = 0
    if y < 0:
        y = GAME_HEIGHT - SPACE_SIZE
    elif y >= GAME_HEIGHT:
        y = 0

    # Add new head of the snake
    snake.coordinates.insert(0, (x, y))
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
    snake.squares.insert(0, square)

    # Check if the snake eats food
    if x == food.coordinates[0] and y == food.coordinates[1]:  # collision with food
        global score
        score += 1
        label.config(text="Score: {}".format(score))

        # Adjust speed after every 3 points
        if score % 3 == 0:
            SPEED = max(20, SPEED - 3)  # Ensure the speed doesn't go below 20

        # Generate new food
        canvas.delete("food")
        food = Food()

        # Generate poison after 10 points if not already present
        if score >= 10 and poison is None:
            poison = Poison()

    else:
        # Remove the last part of the snake if no food is eaten
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    # Check if the snake collides with poison
    if poison and x == poison.coordinates[0] and y == poison.coordinates[1]:
        score -= 3
        poison_collision_count += 1
        label.config(text="Score: {}".format(score))

        # Check if poison collision count reaches 3
        if poison_collision_count >= 3:
            game_over()
            return

        # Remove poison and generate new one after next 10 points
        canvas.delete("poison")
        poison = None

    # Check for collisions with itself
    if check_collisions(snake):
        game_over()
    else:
        window.after(SPEED, next_turn, snake, food, poison)
# change_direction function
def change_direction(new_direction):
    global direction

    if new_direction == 'left' and direction != 'right':
        direction = new_direction
    elif new_direction == 'right' and direction != 'left':
        direction = new_direction
    elif new_direction == 'up' and direction != 'down':
        direction = new_direction
    elif new_direction == 'down' and direction != 'up':
        direction = new_direction

# check_collisions function: Checks if the snake collides with itself
def check_collisions(snake):
    x, y = snake.coordinates[0]

    # Check for self-collision
    if (x, y) in snake.coordinates[1:]:
        print("Game Over: Snake collided with itself")
        return True

    return False

# game_over function: Displays the game over message
def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2,
                       font=('consolas', 70), text="GAME OVER", fill="red", tag="gameover")

# main function: Initializes and runs the game
# Update main function to initialize poison logic
def main():
    global window, canvas, label, direction, score, poison_collision_count  # Added poison_collision_count

    # Initialize the game window and setup basic UI elements
    window = Tk()
    window.title("Snake Game")
    window.resizable(False, False)

    # Initially moving down
    direction = 'down'

    # Score display
    score = 0
    poison_collision_count = 0  # Track number of times snake collides with poison
    label = Label(window, text="Score: {}".format(score), font=('consolas', 40))
    label.pack()

    # Create the game canvas
    global canvas
    canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
    canvas.pack()

    window.update()

    # Center the game window on the screen
    window_width = window.winfo_width()
    window_height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = int((screen_width / 2) - (window_width / 2))
    y = int((screen_height / 2) - (window_height / 2))

    window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Bind arrow keys to change the direction of the snake
    window.bind('<Left>', lambda event: change_direction('left'))
    window.bind('<Right>', lambda event: change_direction('right'))
    window.bind('<Up>', lambda event: change_direction('up'))
    window.bind('<Down>', lambda event: change_direction('down'))

    # Initialize snake, food, and poison objects
    snake = Snake()
    food = Food()

    # Start the game loop with poison initialized as None
    next_turn(snake, food, None)

    window.mainloop()

if __name__ == "__main__":
    main()