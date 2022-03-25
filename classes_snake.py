import random
import os

from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt


class Snake:
    """
    Base snake class.
    """

    def __init__(self, snake_length):
        self.snake_length = snake_length
        self.num_moves = 0
        self.__initialise_snake_body()

    def __initialise_snake_body(self):
        """
        Initialise snake body to line up vertically, one unit apart.
        """

        self.snake_body = []
        snake_head = SnakeBodyPart(0, [0, 0], is_head=True)
        self.snake_body.append(snake_head)
        for i in range(1, self.snake_length):
            body_part = SnakeBodyPart(i, [0, -i])
            self.snake_body.append(body_part)

    def print_snake_info(self):
        """
        Print info for each of the snake's body parts.
        """

        for body_part in self.snake_body:
            body_part.print_info()
        print("")

    def update_body_positions(self):
        """
        Update snake body positions, from tail to head, excluding head.
        """

        for i in range(len(self.snake_body) - 1, 0, -1):
            self.snake_body[i].xpos = self.snake_body[i - 1].xpos
            self.snake_body[i].ypos = self.snake_body[i - 1].ypos

    def move_right(self):
        """
        Move snake one unit right.
        """

        self.update_body_positions()
        self.num_moves += 1
        self.snake_body[0].xpos += 1

    def move_left(self):
        """
        Move snake one unit left.
        """

        self.update_body_positions()
        self.num_moves += 1
        self.snake_body[0].xpos -= 1

    def move_up(self):
        """
        Move snake one unit up.
        """

        self.update_body_positions()
        self.num_moves += 1
        self.snake_body[0].ypos += 1

    def move_down(self):
        """
        Move snake one unit down.
        """

        self.update_body_positions()
        self.num_moves += 1
        self.snake_body[0].ypos -= 1

    def get_head(self):
        """
        Returns the head piece of the snake.
        """

        return self.snake_body[0]

    def plot_snake_position(self):
        """
        Method that plots the position of a snake using matplotlib.imshow..
        """

        # Make a grid
        GRID_SIZE = 50
        plot_grid = np.zeros((GRID_SIZE, GRID_SIZE))

        # plot each snake body part separately
        for body_part in reversed(self.snake_body):

            # move snake to centre of grid
            xpos_centred = body_part.xpos + GRID_SIZE // 2
            ypos_centred = body_part.ypos + GRID_SIZE // 2
            if body_part.is_head:
                plot_grid[xpos_centred, ypos_centred] = 2
            else:
                plot_grid[xpos_centred, ypos_centred] = 1

        plt.figure(figsize=(12, 12))
        plt.imshow(plot_grid)

        if not os.path.isdir("./snake_moves_plots"):
            os.mkdir("./snake_moves_plots")

        plt.savefig(f"./snake_moves_plots/snake_state_{self.num_moves}")

    def move_combo(self, move_tuple, plot_moves=False):
        """
        Given a tuple of moves, performs these snake moves in succesion.
        """

        for move in tqdm(move_tuple):

            # perform move
            if move == "right":
                self.move_right()
            elif move == "left":
                self.move_left()
            elif move == "up":
                self.move_up()
            elif move == "down":
                self.move_down()
            else:
                raise Exception(f"Invalid move: {move}")

            # plot moves
            if plot_moves:
                self.plot_snake_position()


class SnakeBodyPart:
    """
    Class to keep track of the status of each snake body part.
    """

    def __init__(self, ID, initial_pos=[0, 0], is_head=False):
        """
        Base init method
        """

        self.ID = ID
        self.xpos = initial_pos[0]
        self.ypos = initial_pos[1]
        self.is_head = is_head

    def print_info(self):
        """
        Prints info of single snake body part.
        """

        if self.is_head:
            print(
                f'Snake body part of type "head" with ID {self.ID} located at position (x, y) = ({self.xpos}, {self.ypos})'
            )
        else:
            print(
                f"Snake body part with ID {self.ID} located at position (x, y) = ({self.xpos}, {self.ypos})"
            )


def convert_moves_to_string(moves):
    """
    Helper function to convert integer moves to strings.
    """

    str_move = [0] * len(moves)

    for i, move in enumerate(moves):
        if move == 0:
            str_move[i] = "right"
        elif move == 1:
            str_move[i] = "left"
        elif move == 2:
            str_move[i] = "up"
        elif move == 3:
            str_move[i] = "down"
        else:
            raise Exception(f"Invalid move: {move}")

    return str_move


def create_random_moves(n_moves):
    """
    Function that creates a tuple of size n_moves, containing random
    integers between 0 and 3.
    """

    return [random.randint(0, 3) for _ in range(n_moves)]


def main():
    """
    Main snake simulation function.
    """

    snake1 = Snake(snake_length=10)
    random_moves = create_random_moves(n_moves=500)
    random_moves_str = convert_moves_to_string(random_moves)

    snake1.move_combo((random_moves_str), plot_moves=True)


if __name__ == "__main__":
    main()
