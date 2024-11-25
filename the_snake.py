from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
list_dir = (UP, DOWN, LEFT, RIGHT)
# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 5

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """GameObject class description"""

    def __init__(self):
        """Constructor"""
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = None

    def draw(self):
        """Draws the game object"""
        pass

# Описание класса яблока


class Apple(GameObject):
    """Apple class description"""

    def __init__(self):
        super().__init__()
        self.body_color = APPLE_COLOR
        Apple.randomize_position(self)

    # Метод случайного позиционирования яблока
    def randomize_position(self):
        """Randomizes the position of the apple"""
        self.position = (
            randint(0, GRID_WIDTH) * GRID_SIZE,
            randint(0, GRID_HEIGHT) * GRID_SIZE
        )
    # Метод отрисовки яблока

    def draw(self):
        """Draws the apple"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Snake class description"""

    length = 1
    positions: list
    direction = RIGHT
    next_direction = None
    body_color = SNAKE_COLOR
    last = None

    def __init__(self):
        """Constructor"""
        super().__init__()
        self.length = 1
        self.positions = [(self.position)]
        self.direction = choice(list_dir)
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = None

    def get_head_position(self):
        """Returns the head position of the snake"""
        return self.positions[0]

    def update_direction(self):
        """Updates the direction of the snake"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Moves the snake"""
        self.get_head_position()
        head_x, head_y = self.positions[0]
        if self.direction == UP:
            self.positions[0] = (head_x, head_y - 1 * GRID_SIZE)
            if self.positions[0][1] < 0:
                self.positions[0] = (head_x, GRID_HEIGHT * GRID_SIZE)
        if self.direction == DOWN:
            self.positions[0] = (head_x, head_y + 1 * GRID_SIZE)
            if self.positions[0][1] >= GRID_HEIGHT * GRID_SIZE:
                self.positions[0] = (head_x, 0)
        if self.direction == LEFT:
            self.positions[0] = (head_x - 1 * GRID_SIZE, head_y)
            if self.positions[0][0] < 0:
                self.positions[0] = (GRID_WIDTH * GRID_SIZE, head_y)
        if self.direction == RIGHT:
            self.positions[0] = (head_x + 1 * GRID_SIZE, head_y)
            if self.positions[0][0] >= GRID_WIDTH * GRID_SIZE:
                self.positions[0] = (0, head_y)
        self.positions.insert(0, self.positions[0])
        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self):
        """Draws the snake"""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def reset(self):
        """Resets the snake"""
        self.positions = [self.position]
        self.last = None


def handle_keys(game_object):
    """Handles user input"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Main function"""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.

    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()


# Метод draw класса Apple
# def draw(self):
#     rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
#     pygame.draw.rect(screen, self.body_color, rect)
#     pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

# # Метод draw класса Snake
# def draw(self):
#     for position in self.positions[:-1]:
#         rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
#         pygame.draw.rect(screen, self.body_color, rect)
#         pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

#     # Отрисовка головы змейки
#     head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
#     pygame.draw.rect(screen, self.body_color, head_rect)
#     pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

#     # Затирание последнего сегмента
#     if self.last:
#         last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
#         pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

# Функция обработки действий пользователя
# def handle_keys(game_object):
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             raise SystemExit
#         elif event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_UP and game_object.direction != DOWN:
#                 game_object.next_direction = UP
#             elif event.key == pygame.K_DOWN and game_object.direction != UP:
#                 game_object.next_direction = DOWN
#             elif event.key == pygame.K_LEFT and game_object.direction !=
# RIGHT:
#                 game_object.next_direction = LEFT
#             elif event.key == pygame.K_RIGHT and game_object.direction !=
# LEFT:
#                 game_object.next_direction = RIGHT

# Метод обновления направления после нажатия на кнопку
# def update_direction(self):
#     if self.next_direction:
#         self.direction = self.next_direction
#         self.next_direction = None
