import pygame as pg
import random

pg.init()
screen = pg.display.set_mode((1280, 720))
clock = pg.time.Clock()
running = True
font = pg.font.SysFont(None, 32)
pg.key.set_repeat(400, 40)

SIZE = 10
MINE_COUNT = 10
SHOW_MINES = False      # set True while testing to see the mines
minesSet = False
status = None           # None, "win", or "lose"


class Button:
    def __init__(self, x, y, width, height, action=None, action2=None):
        self.rect = pg.Rect(x, y, width, height)
        self.text = ""
        self.is_mine = False
        self.revealed = False
        self.flagged = False
        self.action = action
        self.action2 = action2

    def draw(self, surface):
        if self.flagged:
            color = "green"
        elif self.revealed:
            color = "red" if self.is_mine else "lightblue"
        elif self.is_mine and (SHOW_MINES or status == "lose"):
            color = "purple"
        else:
            color = "blue"
        pg.draw.rect(surface, color, self.rect, border_radius=8)

        if self.text:
            label = font.render(self.text, True, (0, 0, 0))
            surface.blit(label, label.get_rect(center=self.rect.center))

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            if event.button == 1 and self.action:
                self.action(self)
            elif event.button == 3 and self.action2:
                self.action2(self)

class Input:
    def __init__(self,x,y,w,h,action):
        self.rect = pg.Rect(x,y,w,h)
        self.action = action
        self.active = False
        self.text = ""

    def handle_event(self,event):
        if event.type == pg.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)

        if event.type == pg.KEYDOWN and self.active:
            if event.key == pg.K_RETURN:
                if self.action:
                    self.action(self.text)
                self.text = ""
            elif event.key == pg.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode            

    def draw(self, surface):
        border = "white" if self.active else "gray"
        pg.draw.rect(surface, (20, 20, 20), self.rect)
        pg.draw.rect(surface, border, self.rect, width=2)

        # Show only the end of the text if it's too wide for the box
        shown = self.text
        while len(shown) > 3:
            shown = shown[1:]

        label = font.render(shown, True, "white")
        text_pos = (self.rect.x + 10, self.rect.centery - label.get_height() // 2)
        surface.blit(label, text_pos)

def neighbors(index):
    """Indexes of all cells touching `index`, with no wrap-around."""
    row, col = divmod(index, SIZE)
    result = []
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr == 0 and dc == 0:
                continue
            r, c = row + dr, col + dc
            if 0 <= r < SIZE and 0 <= c < SIZE:
                result.append(r * SIZE + c)
    return result


def count_mines(index):
    return sum(buttons[n].is_mine for n in neighbors(index))


def place_mines(safe_index):
    safe = set(neighbors(safe_index)) | {safe_index}
    candidates = [i for i in range(SIZE * SIZE) if i not in safe]
    for i in random.sample(candidates, MINE_COUNT):
        buttons[i].is_mine = True


def reveal(start):
    """Reveal a cell; if it has 0 mines around it, keep spreading outward."""
    stack = [start]
    while stack:
        i = stack.pop()
        b = buttons[i]
        if b.revealed or b.flagged:
            continue
        b.revealed = True
        count = count_mines(i)
        b.text = str(count) if count > 0 else ""
        if count == 0:
            stack.extend(neighbors(i))


def check_for_win():
    # Win = every safe cell has been revealed
    return all(b.revealed for b in buttons if not b.is_mine)


def on_click(button):
    global minesSet, status
    if status is not None or button.revealed or button.flagged:
        return

    index = buttons.index(button)

    if not minesSet:
        place_mines(index)
        minesSet = True

    if button.is_mine:
        button.revealed = True
        status = "lose"
        return

    reveal(index)
    if check_for_win():
        status = "win"


def on_rClick(button):
    if status is not None or button.revealed:
        return
    button.flagged = not button.flagged      # right click toggles the flag


buttons = []
for row in range(SIZE):
    for col in range(SIZE):
        buttons.append(Button(100 + col * 60, 100 + row * 60, 45, 45, on_click, on_rClick))

def rowEnter(input):
    try:
        print(int(input))
    except ValueError:
        print("enter a number")

rows = Input(800,500,30,30,rowEnter)

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        for b in buttons:
            b.handle_event(event)
        rows.handle_event(event)

    screen.fill((30, 30, 30))
    for b in buttons:
        b.draw(screen)
    rows.draw(screen)

    # replaces winButton: gray while playing, green on win, red on loss
    status_color = {"win": "green", "lose": "red"}.get(status, "gray")
    pg.draw.rect(screen, status_color, (800, 100, 90, 90), border_radius=8)

    pg.display.flip()
    clock.tick(60)

pg.quit()