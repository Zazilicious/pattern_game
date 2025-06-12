import pygame
import random
import sys

pygame.init()

# Screen
WIDTH, HEIGHT = 1280, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AA-BB-AA-BB Pattern Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLORS = {
    "red": (255, 0, 0),
    "blue": (0, 0, 255),
    "green": (0, 200, 0),
    "yellow": (255, 255, 0),
    "orange": (255, 165, 0),
    "purple": (160, 32, 240),
    "cyan": (0, 255, 255),
    "pink": (255, 105, 180)
}

# Fonts
font_large = pygame.font.SysFont(None, 48)
font_small = pygame.font.SysFont(None, 36)

# Block settings
BLOCK_SIZE = 100
PADDING = 20
TOP_MARGIN = 150
BOTTOM_MARGIN = 650
SLOT_START_X = WIDTH // 2 - ((BLOCK_SIZE + PADDING) * 4)

# Drag block positions
DRAG_POSITIONS = [
    (WIDTH // 2 - 150, BOTTOM_MARGIN),
    (WIDTH // 2 + 50, BOTTOM_MARGIN)
]

# Setup
clock = pygame.time.Clock()
FPS = 60

def create_new_level():
    """Generate a new AA-BB-AA-BB pattern with 2 random colors."""
    color_names = random.sample(list(COLORS.keys()), 2)
    A, B = COLORS[color_names[0]], COLORS[color_names[1]]
    pattern = [A, A, B, B, A, A, None, None]
    drag_blocks = [
        {"color": A, "pos": list(DRAG_POSITIONS[0]), "rect": pygame.Rect(*DRAG_POSITIONS[0], BLOCK_SIZE, BLOCK_SIZE)},
        {"color": B, "pos": list(DRAG_POSITIONS[1]), "rect": pygame.Rect(*DRAG_POSITIONS[1], BLOCK_SIZE, BLOCK_SIZE)}
    ]
    return pattern, drag_blocks, A, B

def draw_screen(pattern, drag_blocks, message=None, message_color=(0, 150, 0)):
    screen.fill(WHITE)

    title = font_large.render("Complete the Pattern: AA-BB-AA-BB", True, BLACK)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))

    for i in range(8):
        x = SLOT_START_X + i * (BLOCK_SIZE + PADDING)
        y = TOP_MARGIN
        pygame.draw.rect(screen, BLACK, (x, y, BLOCK_SIZE, BLOCK_SIZE), 3)
        if pattern[i]:
            pygame.draw.rect(screen, pattern[i], (x, y, BLOCK_SIZE, BLOCK_SIZE))

    for block in drag_blocks:
        pygame.draw.rect(screen, block["color"], block["rect"])

    if message:
        msg = font_large.render(message, True, message_color)
        screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, BOTTOM_MARGIN - 60))

    pygame.display.flip()

def get_slot_under_mouse(pos, pattern):
    for i in range(6, 8):
        x = SLOT_START_X + i * (BLOCK_SIZE + PADDING)
        y = TOP_MARGIN
        rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
        if rect.collidepoint(pos) and pattern[i] is None:
            return i
    return None

def check_pattern_complete(pattern, B_color):
    return pattern[6] == B_color and pattern[7] == B_color

# Game state
selected_block = None
offset_x, offset_y = 0, 0
pattern, drag_blocks, A_color, B_color = create_new_level()
level_complete = False
fail_message = None
fail_timer = 0
message_timer = 0

running = True
while running:
    current_time = pygame.time.get_ticks()

    if level_complete and current_time - message_timer > 1500:
        pattern, drag_blocks, A_color, B_color = create_new_level()
        level_complete = False
        fail_message = None

    if fail_message and current_time - fail_timer > 1500:
        fail_message = None

    draw_screen(pattern, drag_blocks, message=fail_message if fail_message else ("Great job!" if level_complete else None),
                message_color=(255, 0, 0) if fail_message else (0, 150, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and not level_complete:
            for block in drag_blocks:
                if block["rect"].collidepoint(event.pos):
                    selected_block = block
                    offset_x = block["rect"].x - event.pos[0]
                    offset_y = block["rect"].y - event.pos[1]

        elif event.type == pygame.MOUSEBUTTONUP and selected_block and not level_complete:
            slot_index = get_slot_under_mouse(event.pos, pattern)
            if slot_index is not None:
                # Place temporarily
                pattern[slot_index] = selected_block["color"]
                # Check if it's valid
                if (slot_index == 6 and pattern[6] != B_color) or (slot_index == 7 and pattern[7] != B_color):
                    fail_message = "Try again!"
                    fail_timer = current_time
                    pattern[slot_index] = None
                elif check_pattern_complete(pattern, B_color):
                    level_complete = True
                    message_timer = current_time

            selected_block["rect"].topleft = selected_block["pos"]
            selected_block = None

        elif event.type == pygame.MOUSEMOTION and selected_block:
            selected_block["rect"].x = event.pos[0] + offset_x
            selected_block["rect"].y = event.pos[1] + offset_y

    clock.tick(FPS)

pygame.quit()
sys.exit()
