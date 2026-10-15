import pygame as pg

pg.init()
screen = pg.display.set_mode((1280, 720))
clock = pg.time.Clock()
running = True
font = pg.font.SysFont(None, 32)

def on_click(button):
    buttonindex = buttons.index(button)

    # turns all surrounding cells yellow unless they are already a different color
    try:
        if(buttons[buttonindex+1].state == None):
            buttons[buttonindex+1].state = "yellow"
    except(IndexError):
        pass
 
    try:
        if(buttons[buttonindex+9].state == None):
            buttons[buttonindex+9].state = "yellow"
    except(IndexError):
        pass
    
    try:
        if(buttons[buttonindex+10].state == None):
            buttons[buttonindex+10].state = "yellow"
    except(IndexError):
        pass
    
    try:
        if(buttons[buttonindex+11].state == None):
            buttons[buttonindex+11].state = "yellow"
    except(IndexError):
        pass
    
    try:
        if(buttons[buttonindex-1].state == None):
            buttons[buttonindex-1].state = "yellow"
    except(IndexError):
        pass
    
    try:
        if(buttons[buttonindex-9].state == None):
            buttons[buttonindex-9].state = "yellow"
    except(IndexError):
        pass

    try:
        if(buttons[buttonindex-10].state == None):
            buttons[buttonindex-10].state = "yellow"
    except(IndexError):
        pass

    try:
        if(buttons[buttonindex-11].state == None):
            buttons[buttonindex-11].state = "yellow"
    except(IndexError):
        pass
 
        

class Button:
    COLORS = {
        None: "blue",
        "red": "red",
        "green": "green",
        "yellow": "yellow"
    }

    def __init__(self, x, y, width, height, text, action = None):
        self.rect = pg.Rect(x,y,width,height)
        self.text = text
        self.state = None
        self.action = action

    def draw(self, surface):
        color = self.COLORS[self.state]
        pg.draw.rect(surface, color, self.rect, border_radius=8)

        label = font.render(self.text, True, (255, 255, 255))
        surface.blit(label, label.get_rect(center=self.rect.center))

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.state = "red"
                self.action(self)
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 3:
            if self.rect.collidepoint(event.pos):
                self.state = "green"
                self.action(self)

buttons = []
for i in range(0,600,60):
    for j in range(0,600,60):
        newbutton = Button(100+j,100+i,45,45,"",on_click)
        newbutton.text = str(int(i/60)) + "," + str(int(j/60))
        buttons.append(newbutton)

while(running):

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        for button in buttons:
            button.handle_event(event)

    for button in buttons:
        button.draw(screen)

    pg.display.flip()
    clock.tick(60)

pg.quit()