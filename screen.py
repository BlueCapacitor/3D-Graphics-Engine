'''
Created on Jun 5, 2020

@author: Gosha
'''

from math import pi, sqrt
import turtle

from google.protobuf.internal.factory_test2_pb2 import another_field
from numpy import isfinite, isnan

from geometry import Point


class Screen(object):

    def __init__(self, scale = 200, camera = None):
        self.t = turtle.Pen()
        self.t.hideturtle()

        self.s = self.t.getscreen()
        self.c = self.s.getcanvas()
        self.dCam = camera
        self.scale = scale
        self.window = self.c._root()

        self.s.tracer(0, 0)

        self.t3 = Pen3(self)
#
        self.s.getcanvas()._root().bind("<Up>", lambda _: self.tilt(pi / 32))
        self.s.getcanvas()._root().bind("<Down>", lambda _: self.tilt(0 - pi / 32))
        self.s.getcanvas()._root().bind("<Right>", lambda _: self.turn(pi / 32))
        self.s.getcanvas()._root().bind("<Left>", lambda _: self.turn(0 - pi / 32))

#         self.window.bind('<Motion>', self.mouseMove)

    def unlinkCamera(self):
        self.dCam = None

    def linkCamera(self, camera):
        self.dCam = camera

    def draw(self, Dobject):
        Dobject.draw(self, self.dCam.camera, self.scale)

    def update(self):
        self.t.clear()
        if(self.dCam != None):
            for Dobject in self.dCam.objects:
                self.draw(Dobject)

        self.refresh()

    def refresh(self):
        self.s.update()

    def tilt(self, amount = pi / 16):
        if(self.dCam != None):
            self.dCam.camera.orientation.u += amount

#         self.update()

    def turn(self, amount = pi / 16):
        if(self.dCam != None):
            self.dCam.camera.orientation.v += amount

#         self.update()

    def mouseMove(self, event):
        x, y = event.x, event.y
        if(self.dCam != None):
            self.dCam.camera.orientation.v = (x - self.width() / 2) * 0.01
            self.dCam.camera.orientation.u = 0 - (y - self.height() / 2) * 0.01
            self.dCam.camera.orientation.w = 0

    def checkBounds(self, point2D, margin = (0, 0)):
        if(not(isfinite(point2D[0]) and isfinite(point2D[1]))):
            return(False)

        if(point2D[0] < margin[0] - self.width() * 0.5):
            return(False)
        if(point2D[0] > self.width() * 0.5 - margin[0]):
            return(False)

        if(point2D[1] < margin[1] - self.height() * 0.5):
            return(False)
        if(point2D[1] > self.height() * 0.5 - margin[1]):
            return(False)

        return(True)

    def maxDistToCent(self):
        return(sqrt(self.s.screensize()[0] ** 2 + self.s.screensize()[1] ** 2))

    def width(self):
        return(self.c.winfo_width())

    def height(self):
        return(self.c.winfo_height())

    def updateLoop(self):
        while(True):
            self.update()

    def project(self, point):
        assert self.dCam != None, "No linked camera"
        return(self.dCam.camera.project(point))

    def toScreenCoords(self, point):
        position = self.project(point)
        return([position[0] * self.scale, position[1] * self.scale])

    def target(self, point, other):
        cam = self.dCam.camera
        if(cam.depth(point) < 0.01):
            if(cam.depth(other) < 0.01):
                return

            print
            dilationFactor = cam.depth(other) / (cam.depth(other) - cam.depth(point)) - 0.01

            point = point * dilationFactor + other * (1 - dilationFactor)

        position = self.toScreenCoords(point)

        if(isnan(position[0]) or isnan(position[1])):
            return

#         self.t.goto(*position)

        if(self.checkBounds(position)):
            return((position, None))

        else:
            otherPosition = self.toScreenCoords(other)

            if(isnan(otherPosition[0]) or isnan(otherPosition[1])):
                return

            a, b = position

            c, d = otherPosition

            T, B, R, L = self.height() * 0.5, 0 - self.height() * 0.5, self.width() * 0.5, 0 - self.width() * 0.5

            dilationFactor = 1
            side = None

            if(a < L and a != c):
                if(dilationFactor > (L - c) / (a - c)):
                    dilationFactor = (L - c) / (a - c)
                    side = Side(self, 'L')

            if(a > R and a != c):
                if(dilationFactor > (R - c) / (a - c)):
                    dilationFactor = (R - c) / (a - c)
                    side = Side(self, 'R')

            if(b < B and b != d):
                if(dilationFactor > (B - d) / (b - d)):
                    dilationFactor = (B - d) / (b - d)
                    side = Side(self, 'B')

            if(b > T and b != d):
                if(dilationFactor > (T - d) / (b - d)):
                    dilationFactor = (T - d) / (b - d)
                    side = Side(self, 'T')

            newPosition = dilationFactor * a + (1 - dilationFactor) * c, dilationFactor * b + (1 - dilationFactor) * d
            return((newPosition, side))


class Side(object):

    def __init__(self, screen, side):
        self.screen = screen
        self.side = side

        self.oposites = {'T': 'B', 'B': 'T', 'L': 'R', 'R': 'L'}

    def oposite(self):
        return(Side(self.screen, self.oposites[self.side]))

    def __eq__(self, other):
        return(type(other) == Side and self.screen == other.screen and self.side == other.side)

    def __neq__(self, other):
        return(not(self == other))

    def isOposite(self, other):
        return(self.screen == other.screen and self.side == self.oposites[other.side])

    def isAdjacent(self, other):
        return(self.screen == other.screen and self.side != other.side and self.side != self.oposites[other.side])

    def coord(self):
        if(self.side == 'T'):
            return({'y': self.screen.height() * 0.5})
        if(self.side == 'B'):
            return({'y': 0 - self.screen.height() * 0.5})
        if(self.side == 'R'):
            return({'x': self.screen.width() * 0.5})
        if(self.side == 'L'):
            return({'x': 0 - self.screen.width() * 0.5})

    def intersection(self, other):
        if(not(self.isAdjacent(other))):
            return(None)
        out = self.coord()
        out.update(other.coord())
        return((out['x'], out['y']))


class Pen3(object):

    def __init__(self, screen):
        self.screen = screen
        self.t = screen.t
        self.s = screen.s
        self.point = Point((0, 0, 0))

    def project(self, point):
        assert self.screen.dCam != None, "No linked camera"
        return(self.screen.dCam.camera.project(point))

    def toScreenCoords(self, point):
        position = self.project(point)
        return([position[0] * self.screen.scale, position[1] * self.screen.scale])

    def fakeGoto(self, point, other):
        cam = self.screen.dCam.camera
        if(not(cam.onCamera(point))):
            if(not(cam.onCamera(other))):
                return

            dilationFactor = cam.depth(other) / (cam.depth(other) - cam.depth(point)) - 0.01

            point = point * dilationFactor + other * (1 - dilationFactor)

        position = self.toScreenCoords(point)

        if(isnan(position[0]) or isnan(position[1])):
            return

#         self.t.goto(*position)

        if(self.screen.checkBounds(position)):

            self.t.goto(*position)
        else:
            otherPosition = self.toScreenCoords(other)

            if(isnan(otherPosition[0]) or isnan(otherPosition[1])):
                return

            a, b = position

            c, d = otherPosition

            T, B, R, L = self.screen.height() * 0.5, 0 - self.screen.height() * 0.5, self.screen.width() * 0.5, 0 - self.screen.width() * 0.5

            dilationFactor = 1
            edge = None

            if(a < L and a != c):
                if(dilationFactor > (L - c) / (a - c)):
                    dilationFactor = (L - c) / (a - c)

            if(a > R and a != c):
                dilationFactor = min(dilationFactor, (R - c) / (a - c))

            if(b < B and b != d):
                dilationFactor = min(dilationFactor, (B - d) / (b - d))

            if(b > T and b != d):
                dilationFactor = min(dilationFactor, (T - d) / (b - d))

            newPosition = dilationFactor * a + (1 - dilationFactor) * c, dilationFactor * b + (1 - dilationFactor) * d
            self.t.goto(newPosition)

    def goto(self, point):
        position = self.toScreenCoords(point)
        self.t.goto(*position)
#         cam = self.screen.dCam.camera
#         self.point, oldPoint = newPoint, self.point
#         if(not(cam.onCamera(newPoint)) and not(cam.onCamera(oldPoint))):
#             return
#
#         self.fakeGoto(oldPoint, newPoint)
#         self.fakeGoto(newPoint, oldPoint)

    def down(self):
        self.t.down()

    def up(self):
        self.t.up()

    def begin_fill(self):
        self.t.begin_fill()

    def end_fill(self):
        self.t.end_fill()

    def pencolor(self, *args, **kwargs):
        self.t.pencolor(*args, **kwargs)

    def fillcolor(self, *args, **kwargs):
        self.t.fillcolor(*args, **kwargs)

    def width(self, *args, **kwargs):
        self.t.width(*args, **kwargs)
