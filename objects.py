'''
Created on Jun 5, 2020

@author: Gosha
'''

from geometry import Point, Camera


class Color():

    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    def rgb(self):
        return(self.r, self.g, self.b)


class DPoint(object):

    def __init__(self, point, color = (0, 0, 0), radius = 1):
        self.point = point
        self.color = color
        self.radius = radius

    def draw(self, screen, camera, scale):
        t = screen.t

        cent = camera.project(self.point)
        radius = camera.aproxSphereSize(self.point, self.radius)
        screenDepth = camera.depth(self.point)

        t.up()
        position = [cent[0] * scale, cent[1] * scale]
        if(screenDepth >= 0 and screen.checkBounds(position, (-5, -5))):
            t.goto(*position)
            t.dot(radius * 2 * scale * 0 + 5, self.color)


class DCamera(object):

    def __init__(self, camera, background = (1, 1, 1), objects = []):
        self.camera = camera
        self.background = background
        self.objects = objects

    def show(self, Dobject):
        if(Dobject not in self.objects):
            self.objects.append(Dobject)

    def hide(self, Dobject):
        if(Dobject in self.objects):
            self.objects.remove(Dobject)


class DSurface(object):

    def __init__(self, triangles, fill = (0, 0, 0), border = None):
        self.triangles = triangles
        self.fill = fill
        self.border = border

    def draw(self, screen, *_):
        for triangle in self.triangles:
            self.drawTriangle(triangle, screen)

    def down(self, t):
        if(self.border != None):
            t.pencolor(self.border)
            t.width(2)
            t.down()
        elif(self.fill != None):
            t.pencolor(self.fill)
            t.width(2)
            t.down()

        if(self.fill != None):
            t.fillcolor(self.fill)
            t.begin_fill()

    def drawTriangle(self, triangle, screen):
        t = screen.t
        points = triangle.points

        target = {}
        p = {}
        s = {}

        for a in range(3):
            for b in range(3):
                if(a != b):
                    if(a != b):
                        target[(a, b)] = screen.target(points[a], points[b])

                        if(target[(a, b)] != None):
                            p[(a, b)], s[(a, b)] = target[(a, b)]

        if(all(map(lambda x: x != None, target.values()))):
            t.up()
            t.goto(*p[0, 1])
            self.down(t)

            for a in range(3):
                b = (a + 1) % 3
                c = (a + 2) % 3

                t.goto(*p[(b, a)])
                if(s[(b, a)] != None and s[(b, c)] != None and s[(b, a)].isAdjacent(s[(b, c)])):
                    t.goto(*s[(b, a)].intersection(s[(b, c)]))
                    t.goto(*p[(b, c)])
                else:
                    t.goto(*p[(b, c)])

            t.up()
            t.end_fill()
            return

        elif(all(map(lambda x: x == None, target.values()))):
            return

        for a in range(2):
            for b in range(a + 1, 3):
                if(target[(a, b)] == None):
                    break
            else:
                continue
            break

        c = [[None, 2, 1], [None, None, 0]][a][b]

        if(None in (target[(a, c)], target[(b, c)], target[(c, a)], target[(c, b)])):
            return

        if(s[(a, c)] == s[(b, c)]):
            t.up()
            t.goto(*p[a, c])
            self.down(t)
            t.goto(*p[c, a])
            t.goto(*p[c, b])
            t.goto(*p[b, c])
            t.goto(*p[a, c])
            t.up()
            t.end_fill()
        if(s[(a, c)].isAdjacent(s[(b, c)])):
            t.up()
            t.goto(*p[a, c])
            self.down(t)
            t.goto(*p[c, a])
            t.goto(*p[c, b])
            t.goto(*p[b, c])
            t.goto(*s[b, c].intersection(s[a, c]))
            t.goto(*p[a, c])
            t.up()
            t.end_fill()
        if(s[(a, c)].isOposite(s[(b, c)])):
            o = s[(c, a)].oposite()
            t.up()
            t.goto(*p[a, c])
            self.down(t)
            t.goto(*p[c, a])
            t.goto(*p[c, b])
            t.goto(*p[b, c])
            t.goto(*s[b, c].intersection(o))
            t.goto(*s[a, c].intersection(o))
            t.goto(*p[a, c])
            t.up()
            t.end_fill()
