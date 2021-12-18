import pygame
import sys
import time
# Initiate pygame
pygame.init()
pygame.font.init()

# Sizing constants
WINDOWWIDTH = 1253
WINDOWHEIGHT = 700
BOXSIZE = 8
FIELDWIDTH = 137
FIELDHEIGHT = 70
GAP = 1
XMARGIN = 10
YMARGIN = 10

# Style constants
LIGHTGREY = (225, 225, 225)
DARKGREY = (50, 50, 50)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
BUTTONFONT = pygame.font.SysFont("Courier", 16)
SMALLFONT = pygame.font.SysFont("Courier", 13)

# Set mode for display
DISPLAY = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

def draw_field(alive):
    """
    Draws the boxes for the GUI grid.

    alive -- boxes that should be blue
    """
    for box_x in range(FIELDWIDTH):
        for box_y in range(FIELDHEIGHT):
            left, top = get_box_placement(box_x, box_y)
            if (box_x, box_y) not in alive:
                pygame.draw.rect(DISPLAY, BLACK, (left, top, BOXSIZE, BOXSIZE))
            else:
                pygame.draw.rect(DISPLAY, BLUE, (left, top, BOXSIZE, BOXSIZE))



def get_box_placement(x, y):
    """
    Finds and returns the window coordinates for box (x, y) in the grid.
    """
    left = XMARGIN + (BOXSIZE + GAP) * x
    top = YMARGIN + (BOXSIZE + GAP) * y
    return left, top


def draw_buttons():
    """
    Draw reset, start and speed buttons. Return their collision boxes to check for mouse clicks.
    """
    # Variables that change for each box
    xmargin = [100, WINDOWWIDTH - 200, 30, WINDOWWIDTH - 80]
    widths = [100, 100, 55, 55]
    phrases = ["Reset", "Start", "Slower", "Faster"]

    buttons = []

    for i in range(4):
        button = pygame.Rect(xmargin[i], WINDOWHEIGHT - 50, widths[i], 40)
        text = BUTTONFONT.render(phrases[i], True, BLACK) if i < 2 else SMALLFONT.render(phrases[i], True, BLACK)       # Speed buttons smaller
        rect = text.get_rect()
        rect.center = button.center
        pygame.draw.rect(DISPLAY, LIGHTGREY, button)
        DISPLAY.blit(text, rect)
        buttons.append(button)

    return buttons


def draw_text(error):
    """
    Draw all text in window, including error message if parameter != 0.
    """
    phrases = [
        "Click boxes to create alive squares, then hit start and watch the progression of Conway's Game of Life!",
        "You have not created any alive squares"
    ]

    centers = [
        (WINDOWWIDTH / 2, WINDOWHEIGHT - 40),
        (WINDOWWIDTH / 2, WINDOWHEIGHT - 20)
    ]

    for i in range(2) if error else range(1):      # Only draw error if parameter != 0
        newText = SMALLFONT.render(phrases[i], True, LIGHTGREY if i < 1 else RED)       # Error message in red, all else in grey
        newRect = newText.get_rect()
        newRect.center = centers[i]
        DISPLAY.blit(newText, newRect)


def find_clicked_box(mouse):
    """
    Check if a box has been clicked based on whether its collision rect intersects with mouse coordinates.
    """
    for box_x in range(FIELDWIDTH):
        for box_y in range(FIELDHEIGHT):
            left, top = get_box_placement(box_x, box_y)
            boxSpace = pygame.Rect(left, top, BOXSIZE + GAP, BOXSIZE + GAP)     # Add gap into collision box for some cushion
            if boxSpace.collidepoint(mouse):
                return (box_x, box_y)
    return (None, None)


def pg_events(alive, running, error, buttons, delay):
    """
    Handle any pygame events that occur. Return values that could be influenced by events.

    alive -- set of boxes that are blue, or "alive"
    running -- boolean for whether the game of life is currently running
    error -- boolean to keep track of error messages
    buttons -- list of collision boxes for buttons
    delay -- float time delay in between game actions
    """
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:

            # Reset button clicked
            if buttons[0].collidepoint(event.pos):
                alive = set()
                running = False
                error = False
                delay = 0.5

            # Start button clicked
            if buttons[1].collidepoint(event.pos):
                error = False
                if not alive:
                    error = True
                else:
                    running = True

            # Slower button clicked
            if buttons[2].collidepoint(event.pos):
                if delay <= 0.9:
                    delay += 0.1

            # Faster button clicked
            if buttons[3].collidepoint(event.pos):
                if delay >= 0.1:
                    delay -= 0.1
                
    return alive, running, error, delay


def game_of_life(alive):
    """
    Takes set of "living" boxes as a parameter, implements game of life rules, and returns updated set of "living" boxes.

    Rules:
    Box with < 2 or > 3 alive neighbors dies/remains dead
    Dead box with 3 alive neighbors lives
    Alive box with 2 or 3 alive neighbors lives
    """
    removeList = []
    addList = []

    for box_x in range(FIELDWIDTH):
        for box_y in range(FIELDHEIGHT):

            neighbors = [
                (box_x, box_y + 1),
                (box_x, box_y - 1),
                (box_x - 1, box_y),
                (box_x + 1, box_y),
                (box_x + 1, box_y + 1),
                (box_x - 1, box_y + 1),
                (box_x + 1, box_y - 1),
                (box_x - 1, box_y - 1)
            ]
            aliveNeighbors = []

            # Find all alive neighbors
            for neighbor in neighbors:
                if neighbor in alive:
                    aliveNeighbors.append(neighbor)

            # Dead if < 2 or > 3 neighbors
            if (box_x, box_y) in alive:
                if len(aliveNeighbors) < 2 or len(aliveNeighbors) > 3:
                    removeList.append((box_x, box_y))

            # Alive if 3 neighbors
            else:
                if len(aliveNeighbors) == 3:
                    addList.append((box_x, box_y))

    for box in removeList:
        alive.remove(box)
    for box in addList:
        alive.add(box)

    return alive


def main():
    """
    Main function that controls GUI.
    """
    aliveBoxes = set()
    pygame.display.set_caption("Shortest path")
    error = False
    running = False
    delay = 0.5

    while True:
        # Draw window
        DISPLAY.fill(DARKGREY)
        pygame.draw.rect(DISPLAY, DARKGREY, (XMARGIN, YMARGIN, (BOXSIZE + GAP) * FIELDWIDTH, (BOXSIZE + GAP) * FIELDHEIGHT))
        
        # Control game
        if running:
            time.sleep(delay)
            aliveBoxes = game_of_life(aliveBoxes)

        # Draw components
        draw_text(error)
        buttons = draw_buttons()
        draw_field(aliveBoxes)

        # Handle events
        aliveBoxes, running, error, delay = pg_events(aliveBoxes, running, error, buttons, delay)

        # Handle grid boxes being clicked (Different from pg_events because mouse can be held down with get_pressed)
        if pygame.mouse.get_pressed()[0]:
            mouse = pygame.mouse.get_pos()
            clickedBox = find_clicked_box(mouse)
            if clickedBox[0] is not None:
                aliveBoxes.add(clickedBox)

        pygame.display.update()


if __name__ == "__main__":
    main()