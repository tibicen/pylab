# -*- coding: utf-8 -*-
"""
Created on Fri Feb 27 15:41:57 2015

@author: Tibicen
@contact: dawid.huczynski@gmail.com
@copyright:
@license:
@date:
@version: 0.0.1
"""
from os import listdir
from random import random, randrange
from math import sin, cos, radians, sqrt, pi
import matplotlib.pyplot as plt
from matplotlib.colors import hsv_to_rgb

__author__ = "Tibicen"
__copyright__ = "Copyright 2014"
STOP = False
SAVE = False
TARGET = (0, 5000)
ROUNDS = 1
WALKERS_COUNT = 500
COLOR = True


def length(pos1, pos2):
    deltax = abs(pos1[0] - pos2[0])
    deltay = abs(pos1[1] - pos2[1])
    return sqrt(deltax**2 + deltay**2)


# MATPLOT INTERACTION


def onkey(event):
    global SAVE
    global STOP
    print('you pressed', event.key, event.xdata, event.ydata)
    if event.key == 'q':
        STOP = not STOP
        if STOP:
            print('system will stop.')
        else:
            print('system will continue.')
    elif event.key == 'z':
        SAVE = not SAVE


def onclick(event):
    print('button=%d, x=%d, y=%d, xdata=%f, ydata=%f' % (
        event.button, event.x, event.y, event.xdata, event.ydata))


class Walker(object):

    def __init__(self, name, pos=(0, 0), angle=60):
        self.name = name
        self.xdata = [pos[0]]
        self.ydata = [pos[1]]
        self.vector = radians(randrange(0, 361))
        self.angle = angle
        self.angle_change = 2
        self.deltaT = []  # positive values shows it walks thowards target
        if COLOR:
            self.color = (random() * 0.8, random() * 0.8, random() * 0.8)
            self.color = hsv_to_rgb((random(), .8, .9))
        else:
            i = random() * .7 + .1
            self.color = (i, i, i)
        self.line, = plt.plot(self.xdata, self.ydata,
                              color=self.color, linewidth=.5, alpha=.5)
        # self.text = plt.text(pos[0], pos[1], str(
        #     name), fontsize=10, color=self.color)

    def setTarget(self, target):
        self.target = target

    def getPos(self):
        pos = (self.xdata[-1], self.ydata[-1])
        return pos

    def move(self):
        # TODO Find out why walks are more CW direction rather than CCW
        pos = (self.xdata[-1], self.ydata[-1])
        lenA = length(pos, self.target)
        # checks if is enought history rounds
        # print('{:000.4f}\t{}'.format(self.vector, self.angle))
        if len(self.deltaT) < 3:
            self.vector = self.vector + \
                radians(randrange(-self.angle, self.angle + 1))
        else:
            # narrowing or widening target direction
            # if  0.1 < abs(self.deltaT[-1] - self.deltaT[-2]) - abs(self.deltaT[-2] - self.deltaT[-3]):
            #     self.angle = 2
            #     self.angle_change = 2
            if self.deltaT[-1] - self.deltaT[-2] < self.deltaT[-2] - self.deltaT[-3]:
                self.angle_change -= .1
            else:
                self.angle_change += .1
            # if deltaT < 0 further
            # elif deltaT > 0 closer
            if self.deltaT[-1] < 0:  # walks away
                if self.angle < 32:
                    self.angle += 1
            else:  # walks closer
                if self.angle > 2:
                    self.angle -= 1
            if not 0 < self.deltaT[-1] - self.deltaT[-2] < .00001:
                # not perfect direction, vector change
                self.vector = self.vector + \
                    radians(randrange(-self.angle, self.angle + 1))
        newPos = (self.xdata[-1] + cos(self.vector),
                  self.ydata[-1] + sin(self.vector))
        lenB = length(newPos, self.target)
        self.deltaT.append(lenA - lenB)
        self.xdata.append(newPos[0])
        self.ydata.append(newPos[1])
        self.line.set_data(self.xdata, self.ydata)
        # self.text.set_position((self.xdata[-1], self.ydata[-1]))
        if lenB < .2:
            print('Walker %d got to the target.' % (self.name))
            print('He walked %d.' % (len(self.xdata) - 1))
            return self.line, True
        return self.line, False

    def checkDirection(self, target):
        pos = (self.xdata[-1], self.ydata[-1])
        return length(pos, target)


class ArtWalker(Walker):

    def __init__(self, name, pos=(0, 0), angle=60):
        Walker.__init__(self, name, pos, angle)
        self.vector = radians(180 * name / WALKERS_COUNT)
        # self.vector = radians(90)
        if COLOR:
            self.color = hsv_to_rgb(((name / WALKERS_COUNT) / 3.6, .8, 1))
        else:
            i = .1 + .7 * sin(pi * name / WALKERS_COUNT)
            self.color = (i, i, i)
        self.line, = plt.plot(self.xdata, self.ydata,
                              color=self.color, linewidth=.5, alpha=.5)


def initPlot(ranges=10):
    global refresh
    step = 0
    xmin, xmax = [-1 * ranges, ranges]
    ymin, ymax = [-1 * ranges, ranges]
    ax = plt.axes(xlim=(xmin, xmax), ylim=(ymin, ymax))
    refresh = 1
    speedTxt = plt.text(0.01, 0.99, 'Speed: ' + str(refresh),
                        ha='left', va='top', transform=ax.transAxes)
    timeTxt = plt.text(0.01, 0.95, 'Round: ' + str(step),
                       ha='left', va='top', transform=ax.transAxes)
#    v = [0 for x in range(-5,5)]
#    pion, = plt.plot(v, color=(1,0,0,0.5), linestyle='dashed')
#    poziom, = plt.plot(v, color=(1,0,0,0.5), linestyle='dashed')
#    maxLine, = plt.plot(v, color=(0,0,1,0.5), linestyle='dashed')
#    minLine, = plt.plot(v, color=(0,0,1,0.5), linestyle='dashed')
    plt.ion()
    plt.grid()
    plt.connect('key_press_event', onkey)
    plt.show()
    return ax, speedTxt, timeTxt, step, refresh, (xmin, xmax, ymin, ymax)


def walks(walkers, plt, ax, maxs, step):
    global refresh
    global SAVE
    xmin, xmax, ymin, ymax = maxs
    ax.set_aspect('equal')
    ax.margins(.1)
    got = False
    while True:
        for walker in walkers:
            line, temp = walker.move()
            if temp:
                got = True
            x, y = walker.getPos()
            if xmax < x:
                xmax = x + x / 3
            if xmin > x:
                xmin = x + x / 3
            if ymax < y:
                ymax = y + y / 3
            if ymin > y:
                ymin = y + y / 3
        plt.xlim([xmin, xmax])
        plt.ylim([ymin, ymax])
        if step in [50, 400, 10000, 70000]:
            refresh = refresh * 10
            speedTxt.set_text('Speed: ' + str(refresh))
            plt.draw()
            plt.pause(0.0000001)
        if step % refresh == 0:
            timeTxt.set_text('Round: ' + str(step))
            plt.draw()
            plt.pause(0.0000001)
        if got:
            timeTxt.set_text('Round: ' + str(step))
            speedTxt.set_text('Speed: ' + str(refresh))
            plt.draw()
            nr = 0
            for x in listdir():
                if x.startswith('walkers') and not x.endswith('.py'):
                    nr = max(nr, int(x.split('.')[0][-3:]))
                name = 'walkers' + '{:03d}'.format(nr + 1)
            for format in ('png', 'svg', 'pdf'):
                plt.savefig(name + '.' + format)
            plt.pause(0.0000001)
            break
        if STOP:
            nr = 0
            for x in listdir():
                if x.startswith('walkers') and not x.endswith('.py'):
                    nr = max(nr, int(x.split('.')[0][-3:]))
                name = 'walkers' + '{:03d}'.format(nr + 1)
            for format in ('png', 'svg', 'pdf'):
                plt.savefig(name + '.' + format)
            break
        if SAVE:
            print('Saving...', end='')
            nr = 0
            for x in listdir():
                if x.startswith('walkers') and not x.endswith('.py'):
                    nr = max(nr, int(x.split('.')[0][-3:]))
                name = 'walkers' + '{:03d}'.format(nr + 1)
            for format in ('png', 'svg', 'pdf'):
                plt.savefig(name + '.' + format)
            SAVE = False
            print('saved.')
        step += 1


ax, speedTxt, timeTxt, step, refresh, (xmin, xmax, ymin, ymax) = initPlot()
maxs = (xmin, xmax, ymin, ymax)
targetCircle = plt.Circle(TARGET, max(TARGET) / 50, color=(1, 0, 0), zorder=10)
ax.add_artist(targetCircle)
# walkers = [Walker(x, (0, 0)) for x in range(WALKERS_COUNT)]
walkers = [ArtWalker(x, (0, 0), 2) for x in range(WALKERS_COUNT)]
for w in walkers:
    w.setTarget(TARGET)
for n in range(ROUNDS):
    # TARGET = (randrange(-100, 101), randrange(-100, 101))
    walks(walkers, plt, ax, maxs, step)
    for w in walkers:
        w.xdata = [w.xdata[-1]]
        w.ydata = [w.ydata[-1]]
        w.setTarget(TARGET)
        # print('Walker at (%d, %d)' % (w.xdata[0], w.ydata[0]))
        targetCircle.get_transform()
