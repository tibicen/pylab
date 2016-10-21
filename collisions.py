# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 23:29:32 2015

@author: tibicen
"""

import matplotlib.pyplot as plt
import colorsys as colors
from random import random, randrange
from math import sin, cos, radians, sqrt, atan
# import matplotlib.colors as colors


def onclick(event):
    global circles
    if event.button == 1:
        for circle in circles:
            circle.target = (event.xdata, event.ydata)
    elif event.button == 3:
        for circle in circles:
            circle.center = circle.center[
                0] + 30 * random() - 15, circle.center[1] + 30 * random() - 15
    print('button=%d, x=%d, y=%d, xdata=%f, ydata=%f' % (
        event.button, event.x, event.y, event.xdata, event.ydata))


def length(pos1, pos2):
    deltax = abs(pos1[0] - pos2[0])
    deltay = abs(pos1[1] - pos2[1])
    return sqrt(deltax**2 + deltay**2)


def middle(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    dx, dy = abs(x1 - x2), abs(y1 - y2)
    xm = min(x1, x2) + dx
    ym = min(y1, y2) + dy
    return ((xm, ym), (dx, dy))


def checkCollision(elements):
    for element1 in elements:
        for element2 in elements:
            l = length(element1.center, element2.center)
            rr = element1.radius + element2.radius
            if element1 == element2:
                continue
            elif l < rr:
                x1, y1 = element1.center
                x2, y2 = element2.center
                if x1 == x2:
                    angle = radians(90)
                else:
                    a = (y1 - y2) / (x1 - x2)
                    angle = atan(a)
                newPos1 = (x1 + cos(angle) * (rr - l) /
                           2 + (random() - .5) / 100, y1 + sin(angle) *
                           (rr - l) / 2 + (random() - .5) / 100)
                newPos2 = (x2 - cos(angle) * (rr - l) / 2 + (random() - .5) /
                           100, y2 - sin(angle) * (rr - l) / 2 +
                           (random() - .5) / 100)
                element1.center = newPos1
                element2.center = newPos2


class Walker(plt.Circle):

    def move(self):
        if self.center != self.target:
            x1, y1 = self.center
            x2, y2 = self.target
            a = (y1 - y2) / (x1 - x2)
            angle = atan(a)
            self.vector = angle
            dist = 1
            if self.radius < 1:
                dist = self.radius
            if x1 < x2:
                newPos = (x1 + cos(self.vector) * dist,
                          y1 + sin(self.vector) * dist)
            else:
                newPos = (x1 - cos(self.vector) * dist,
                          y1 - sin(self.vector) * dist)
            if length(self.center, self.target) < length(self.center, newPos):
                newPos = self.target
            self.center = newPos
            self.text.set_position(newPos)
            self.text.set_horizontalalignment('center')
            self.text.set_verticalalignment('center')

    def setText(self, text):
        self.text = text

    def checkDirection(self, target):
        pass

    def setTarget(self, target):
        self.target = target

r = 100
xmin, xmax = -r, r
ymin, ymax = -r, r
ax = plt.axes(xlim=(xmin, xmax), ylim=(ymin, ymax))

plt.ion()
plt.grid()
plt.show()
ax.set_aspect('equal')
ax.margins(.1)
plt.connect('button_press_event', onclick)
target = (0, 0)
plt.show()

circles = []
texts = []
top = 30
for n in range(top):
    x, y = random() * 40 - 20, random() * 40 - 20
#    x,y = 6*n, 0
#    r = random()*4+1
    r = 3
    circles.append(Walker((x, y), randrange(2, 10),
                          color=colors.hsv_to_rgb(n / float(top),
                                                  .4 + .3 * random(),
                                                  .6 + .2 * random())))
    texts.append(plt.Text(x, y, str(n), verticalalignment='center',
                          horizontalalignment='center', color=(1, 1, 1)))
    circles[-1].setTarget((0, 0))
    circles[-1].setText(texts[-1])
    ax.add_artist(circles[-1])
    ax.add_artist(texts[-1])
#    for n in circles:
#        n.radius = n.radius + (random() - .5)*.5
#    plt.draw()
#    plt.pause(0.0000000000000000000001)


rounds = 0
timeTxt = plt.text(0.01, 0.95, 'Round: ' + str(rounds), ha='left', va='top',
                   transform=ax.transAxes)
while True:
    rounds += 1
    checkCollision(circles)
    for w in circles:
        w.move()
        checkCollision(circles)
        checkCollision(circles)
        if w.center[0] > xmax:
            xmax = w.center[0]
        ax.xlim = (0, xmax)
    if rounds % 1 == 0:
        timeTxt.set_text('Round: ' + str(rounds))
        plt.draw()
        plt.savefig('collisions\\collisions_{:03d}.png'.format(rounds))
        plt.pause(0.00000000000000000000000001)


for n in circles:
    print(n.vector)
