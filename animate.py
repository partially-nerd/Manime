from sys import argv
from pygame import Color, font, display, init, QUIT, quit as pgquit, event, Surface, Rect, image, time
from pygame.draw import rect as rectangle, circle
from math import floor 
from time import sleep

class ColorPalette:
    bg                = Color(17, 20, 26)
    red               = Color(217, 62, 41)
    green             = Color(50, 168, 82)
    blue              = Color(94, 155, 219)
    blue_dark         = Color(74, 135, 200)
    purple            = Color(129, 94, 219)
    brown             = Color(79, 38, 30)
    orange            = Color(255, 107, 33)
    yellow            = Color(227, 224, 61)
    gray              = Color(26, 26, 26)
    gray_light        = Color(69, 69, 69)

class Object:
    w                 = 200
    h                 = 200
    x                 = 0
    y                 = 0
    br_w              = 3
    opacity           = 50
    br_rd             = 10
    t                 = 0

    def reset_pos(self):
        self.t = 0
        globals()["INT_RET"] = True
    
    def reset_neg(self):
        self.t = 1
        globals()["INT_RET"] = True

    def interpolate(self, param, start, end, lerp = lambda t:t ** (1/2) * (1 - t) +  t ** 2):
        if start > end:
            start2, end2 = end,start
        else:
            start2, end2 = start, end
        t = lerp(self.t)
        self.__setattr__(param, start2 * (1 - t ) + end2 * t)
        if start > end:
            self.t -= 0.006
            if self.t <= 0:
                globals()["INT_RET"] = True
            else:
                globals()["INT_RET"] = False
        else:
            self.t += 0.006
            if self.t >= 1:
                globals()["INT_RET"] = True
            else:
                globals()["INT_RET"] = False

    def __init__(self, id, parent, kwargs) -> None:
        self.id = id

        self.parent   = parent
        self.parent.children.append(self)
        self.br_bg    = self.parent.colors.blue
        self.bg       = self.parent.colors.bg
        globals()[self.id] = self

        self.__kwargs__(kwargs=kwargs)

    def __kwargs__(self, kwargs):
        for kwarg in kwargs.keys():
            self.__setattr__(kwarg,kwargs[kwarg])

class Rectangle(Object):
    def __init__(self, id, parent, kwargs) -> None:
        super().__init__(id, parent, kwargs)

    def draw(self):
        self.obj = Surface((self.w,self.h))
        center = (
            self.x+(self.parent.w-self.obj.get_width())/2,
            self.y+(self.parent.h-self.obj.get_height())/2
        )
        self.obj.set_alpha(self.opacity)
        self.obj.fill(self.bg, rect=Rect(self.x+self.br_w, self.y+self.br_w ,abs(self.w - 2 * self.br_w), abs(self.h - 2 * self.br_w)))
        self.obj.set_alpha(100)
        self.obj.fill(self.br_bg, rect=Rect(self.x, self.y, abs(self.w), abs(self.h)))
        self.parent.display.blit(self.obj, center)

class RoundedRectangle(Object):
    def __init__(self, id, parent, kwargs) -> None:
        super().__init__(id,parent, kwargs)

    def draw(self):
        center = (
            self.x+(self.parent.w-self.w)/2,
            self.y+(self.parent.h-self.h)/2
        )
        rectangle(self.parent.display, self.br_bg, (*center, abs(self.w), abs(self.h)), width=self.br_w, border_radius=self.br_rd)
        rectangle(self.parent.display, self.bg, (center[0]+self.br_w, center[1]+self.br_w ,abs(self.w) - 2 * self.br_w, abs(self.h) - 2 * self.br_w), border_radius=self.br_rd)

class Circle(Object):
    def __init__(self, id, parent, kwargs):
        self.r = 50
        super().__init__(id, parent, kwargs)

    def draw(self):
        center = (
            floor(self.x+self.parent.w/2),
            floor(self.y+self.parent.h/2)
        )
        circle(self.parent.display, color=self.br_bg, radius=self.r, center=center, width=self.br_w)
        circle(self.parent.display, color=self.bg, radius=self.r-2*self.br_w, center=center)

class Window:
    w = 400
    h = 400
    frame_no = 1
    colors = ColorPalette()
    clock = time.Clock()
    is_alive = True
    children = []

    def __init__(self, **kwargs) -> None:
        init()
        self.__kwargs__(kwargs=kwargs)
        
        self.display = display.set_mode((self.w, self.h))

    def __kwargs__(self, kwargs):
        for kwarg in kwargs.keys():
            self.__setattr__(kwarg,kwargs[kwarg])

    def draw_all(self):
        for i in self.children:
            i.draw()

    def play_animations(self):
        for i in self.queue_animations:
            if len(i) > 1:
                for j in i:
                    loc = {}
                    exec(j) 
                    if globals()["INT_RET"] == True:
                        self.queue_animations.pop(0)
                        return
                return
            else:
                exec(i[0])
                if globals()["INT_RET"] == True:
                    self.queue_animations.pop(0)
                return

    def draw_rectangle(self, id, **kwargs):
        return Rectangle(id, self, kwargs)

    def draw_rounded_rectangle(self, id, **kwargs):
        return RoundedRectangle(id, self, kwargs)

    def draw_circle(self, id, **kwargs):
        return Circle(id, self, kwargs)

    def render(self, callback):
        if "--save" in argv:
            while self.is_alive:
                self.display.fill(self.colors.bg)

                for eve in event.get():
                    if eve.type==QUIT:
                        pgquit()
                        quit()

                callback()
                image.save(win.display, f"./frames/frame{win.frame_no}.png")

                self.frame_no += 1
                self.clock.tick(60)
                display.flip()
        else:
            while self.is_alive:
                self.display.fill(self.colors.bg)

                for eve in event.get():
                    if eve.type==QUIT:
                        pgquit()
                        quit()

                callback()

                self.clock.tick(60)
                display.flip()

def draw():
    rect.h -= 1
    if circ.y >= win.h/2-circ.r:
        circ.y -= 100
    else:
        circ.y += 1
    rect.draw()
    circ.draw()

if __name__ == '__main':
    win = Window()
    rect = win.draw_rounded_rectangle()
    circ = win.draw_circle()
    win.render(draw)
