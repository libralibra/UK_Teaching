from typing import Any
import pygame
import random

# Define colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Initialize Pygame
pygame.init()

# Set up the display
win_size = (800, 600)
window = pygame.display.set_mode(win_size)
pygame.display.set_caption("Behavior Tree Demo")

# Character properties
char_pos = [50, 50]
char_radius = 15
char_speed = 1

# Obstacle properties
obstacles = [
    pygame.Rect(200, 200, 100, 20),
    pygame.Rect(400, 300, 20, 150),
    pygame.Rect(100, 500, 150, 20)
]

# Goal properties
goal_pos = [700, 500]
goal_radius = 20

# Initialize clock
clock = pygame.time.Clock()

# Behavior Tree Functions


def move_towards_goal():
    global char_pos
    char_x, char_y = char_pos
    goal_x, goal_y = goal_pos

    if char_x < goal_x:
        char_x += char_speed
    elif char_x > goal_x:
        char_x -= char_speed

    if char_y < goal_y:
        char_y += char_speed
    elif char_y > goal_y:
        char_y -= char_speed

    char_pos = [char_x, char_y]
    return True


def check_collision(pos, radius, rect):
    ''' return true if the character position intersects the rectangle [x,y,w,h] '''
    char_x, char_y = char_pos
    char_rect = pygame.Rect(char_x - char_radius, char_y -
                            char_radius, char_radius * 2, char_radius * 2)
    return char_rect.colliderect(rect)


def avoid_obstacles():
    global char_pos
    char_x, char_y = char_pos

    for obstacle in obstacles:
        if check_collision(char_pos, char_radius, obstacle):
            # If collision, try different directions
            for _ in range(3):
                char_x += random.choice([-1, 1]) * char_speed
                char_y += random.choice([-1, 1]) * char_speed
                char_pos = [char_x, char_y]
                if not check_collision(char_pos, char_radius, obstacle):
                    return True

            return False

    return False


def random_movement():
    global char_pos
    temp_pos = [x+char_speed for x in char_pos]
    for obstacle in obstacles:
        if not check_collision(temp_pos, char_radius, obstacle):
            char_pos = temp_pos
            return True
        else:
            return False
    char_pos = temp_pos
    return True

# Behavior Tree Nodes


class ActionNode:
    def __init__(self, func) -> None:
        self.func = func

    def execute(self) -> bool:
        return self.func()

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self.execute()


class SequenceNode:
    def __init__(self, nodes):
        self.nodes = nodes

    def execute(self):
        for node in self.nodes:
            if not node():
                return False
        return True

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self.execute()


class SelectorNode:
    def __init__(self, nodes):
        self.nodes = nodes

    def execute(self):
        for node in self.nodes:
            if node():
                return True
        return False

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self.execute()


# Main loop
running = True
while running:
    window.fill(WHITE)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw obstacles
    for obstacle in obstacles:
        pygame.draw.rect(window, BLACK, obstacle)

    # Draw goal
    pygame.draw.circle(window, RED, goal_pos, goal_radius)

    # Draw character
    pygame.draw.circle(window, BLACK, char_pos, char_radius)

    # Behavior Tree Setup
    tree = SelectorNode([
        SequenceNode([ActionNode(move_towards_goal),
                     ActionNode(avoid_obstacles)]),
        ActionNode(random_movement)
    ])
    tree.execute()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
