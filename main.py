'''
Created on Jun 5, 2020

@author: Gosha
'''

from geometry import Point, Camera, Direction, Triangle
from objects import DPoint, DCamera, DSurface
from screen import Screen

if(__name__ == '__main__'):
    cam = Camera(Point((0, 0, 0)), Direction((0, 0, 0)))
    dCam = DCamera(cam)
    screen = Screen()
    screen.linkCamera(dCam)

    sides = []

    sides.append(DSurface([Triangle(Point((-10, 10, 10)), Point((10, 10, 10)), Point((10, 10, -10))),
                           Triangle(Point((-10, 10, 10)), Point((-10, 10, -10)), Point((10, 10, -10)))], (1, 1, 0), (0, 0, 0)))
    sides.append(DSurface([Triangle(Point((-10, -10, 10)), Point((10, -10, 10)), Point((10, -10, -10))),
                           Triangle(Point((-10, -10, 10)), Point((-10, -10, -10)), Point((10, -10, -10)))], (0.5, 0.5, 0.5), (0, 0, 0)))
    sides.append(DSurface([Triangle(Point((10, -10, 10)), Point((10, 10, 10)), Point((10, 10, -10))),
                           Triangle(Point((10, -10, 10)), Point((10, -10, -10)), Point((10, 10, -10)))], (0, 1, 0), (0, 0, 0)))
    for side in sides:
        dCam.show(side)

    for x in [-10, 10]:
        for y in [-10, 10]:
            for z in [-10, 10]:
                dCam.show(DPoint(Point((x, y, z))))

    screen.updateLoop()

    print("done")
    screen.s.mainloop()
