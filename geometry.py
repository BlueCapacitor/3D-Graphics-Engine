'''
Created on Jun 5, 2020

@author: Gosha
'''

from math import sin, cos, sqrt

from numpy import array, nan, isfinite


class Point(object):

    def __init__(self, coords):
        self.x = float(coords[0])
        self.y = float(coords[1])
        self.z = float(coords[2])

    def toVector(self):
        return(array([[self.x], [self.y], [self.z]]))

    def norm(self):
        return(sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2))

    def isfinite(self):
        return(isfinite(self.x) and isfinite(self.y) and isfinite(self.z))

    def __add__(self, other):
        return(Point((self.x + other.x, self.y + other.y, self.z + other.z)))

    def __sub__(self, other):
        return(Point((self.x - other.x, self.y - other.y, self.z - other.z)))

    def __mul__(self, scale):
        return(Point((self.x * scale, self.y * scale, self.z * scale)))

    def __rmul__(self, scale):
        return(Point((self.x * scale, self.y * scale, self.z * scale)))

    def __truediv__(self, scale):
        return(Point((self.x / scale, self.y / scale, self.z / scale)))

    def __getitem__(self, i):
        return([self.x, self.y, self.z][i])

    def __str__(self):
        return("Point(%s, %s, %s)" % (self.x, self.y, self.z))


class Direction(object):

    def __init__(self, angle):
        self.u = angle[0]
        self.v = angle[1]
        self.w = angle[2]


class Camera(object):

    def __init__(self, location, orientation, distance = 1):
        self.location = location
        self.orientation = orientation
        self.distance = distance

    def tMatrix(self):
        t = self.orientation
        AU = array([[1, 0, 0],
                    [0, cos(t.u), -sin(t.u)],
                    [0, sin(t.u), cos(t.u)]])
        UV = array([[cos(t.v), 0, -sin(t.v)],
                    [0, 1, 0],
                    [sin(t.v), 0, cos(t.v)]])
        UW = array([[cos(t.w), -sin(t.w), 0],
                    [sin(t.w), cos(t.w), 0],
                    [0, 0, 1]])

        return(AU.dot(UV).dot(UW))

    def translate(self, point):
        dif = point - self.location
        D = Point(self.tMatrix().dot(dif.toVector()))
        return(D)

    def depth(self, point):
        return(self.translate(point).z)

    def aproxSphereSize(self, cent, r):
        cam = self.location
        dy = (cent.y - cam.y)
        dx = (cent.x - cam.x)

        perpendicularVector = Point((0 - dy, dx, 0))
        if(perpendicularVector.norm() == 0):
            perpendicularVector = Point((0, 1, 0))
        aproxTanPoint = cent + perpendicularVector / perpendicularVector.norm() * r

        Pcent = self.project(cent)
        PaTan = self.project(aproxTanPoint)
        return((Pcent[0] - PaTan[0]) ** 2 + (Pcent[1] - PaTan[1]) ** 2)

    def distance(self, point):
        return((self.location - point).norm)

    def project(self, point):
        D = self.translate(point)
        r = self.distance / D.z if D.z != 0 else nan

        return((r * D)[:2])

    def onCamera(self, point):
        return(self.depth(point) > 0)


class Triangle(object):

    def __init__(self, A, B, C):
        self.points = [A, B, C]
