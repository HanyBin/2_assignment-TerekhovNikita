from tkinter import Tk, Canvas
import time
from math import sin, cos, radians, pi
from PIL import Image, ImageTk, ImageDraw
from random import randint


SIZE = 600
CENTER = SIZE / 2
SUN_R = 50

class Planet(object):
    def __init__ (self, distance, radius, speed = 0, clockwise = True, canvas = None,
                  parent_planet = None, pivot = None, alpha = 0.8, color = "grey"):
        self.pivot = pivot
        self.canvas = canvas
        self.alpha = alpha
        self.color = color
        self.parent = parent_planet
        self.r = radius
        self.d = distance
        self.speed = speed
        self.clockwise =  clockwise
        self.coords = self.x_y()
        self.oval = self.create_oval()


    def tnow(self):
        return radians((time.time() % 3600) / 10 * self.speed)

    def x_y(self):
        rad = self.tnow()
        x0, y0 = self.pivot if self.pivot else self.parent.coords
        if self.clockwise:
            x = x0 + (self.d + self.r) * cos(rad - pi / 2)
            y = y0 + (self.d + self.r) * sin(rad - pi / 2)
        else:
            x = x0 + (self.d + self.r) * sin(rad + pi)
            y = y0 + (self.d + self.r) * cos(rad + pi)
        return [x, y]

    def create_oval(self):

        size = self.r * 2 + 1
        img_alpha = Image.new("L", (size, size), 0)
        draw = ImageDraw.Draw(img_alpha)
        draw.ellipse((0, 0, size - 1, size - 1), fill = int(255 * self.alpha))
        img_oval = Image.new('RGB', (size, size), self.color)
        img_oval.putalpha(img_alpha)
        img_tk = ImageTk.PhotoImage(img_oval)
        self.canvas.images.append(img_tk)
        obj_id = self.canvas.create_image(
            self.coords[0],
            self.coords[1],
            image = img_tk,
            anchor = "center"
            )
        return obj_id


def create_asteroid_belt(count, parent):
    asteroid_belt = []
    for _ in range(count):
        speed = randint(300, 600)
        size = randint(3, 10)
        distance = randint(45, 60)
        clockwise = bool(randint(0,1))
        asteroid = Planet(distance, size, speed, clockwise, canvas, parent)
        asteroid_belt.append(asteroid)
    return asteroid_belt

root = Tk()

canvas = Canvas(
    root,
    width=SIZE,
    height=SIZE,
    bg="white"
    )
canvas.images = []
canvas.pack()

sun = Planet( 0, SUN_R, canvas = canvas, color = 'yellow', alpha = 1, pivot = [CENTER, CENTER + SUN_R])


planets = [
    Planet(100, 7, 120, True, canvas, sun),
    Planet(200, 15, 60, True, canvas, sun),
    Planet(150, 30, 400, False, canvas, sun, color = "red", alpha = 0.5),
]
planets.extend((
    Planet(15, 2, 240, True, canvas, planets[0]),
    Planet(12, 5, 360, False, canvas, planets[0]),
    Planet(19, 3, 150, False, canvas, planets[0]),
))

planets.extend(create_asteroid_belt(10, planets[2]))

print(planets)
def motion():
    for planet in planets:
        coords = planet.x_y()
        canvas.move(
            planet.oval,
            coords[0] - planet.coords[0],
            coords[1] - planet.coords[1]
            )

        planet.coords = coords
    root.after(10, motion)
motion()


root.mainloop()
