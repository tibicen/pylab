# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 18:47:49 2013

@author: tibicen
"""
import time
import random
from scipy.optimize import fsolve
import pylab as plt
import itertools as it
import os
print(os.getcwd())
from math import sqrt
from scipy.spatial import Voronoi, voronoi_plot_2d
pi = 3.141592653589793
plt.clf()
class Shape():
    def __init__(self, name, area, nodes=[], deps=[]):
        self.name = name
        self.area = area
        self.nodes = nodes
        self.loc = None
        self.deps = deps
        self.radius = sqrt(area/3.141592653589793)
        
    def getArea(self):
        return self.area
    
    def getName(self):
        return self.name
    
    def getRadius(self):
        return self.radius
            
    def getLoc(self):
        return self.loc
        
    def getNodes(self):
        return self.nodes
        
    def addNode(self, nodelist):
        for node in nodelist:
            if node not in self.nodes:
                self.nodes.append(node)
    
    def delNode(self, name):
        for node in self.nodes:
            if node.name == name:
                self.nodes.remove(node)
                print('Node removed')
                break
    
    def insertLoc(self, x,y):
        self.loc = (x,y)
    
    def __repr__(self):
        if self.loc:
            return "Shape %s[(%.2f,%.2f) r=%.2f]" % (self.name, self.loc[0], 
                             self.loc[1], self.radius)
        else:
            return "Shape %s[r=%.2f]" % (self.name, self.radius)


#  (x3-x1)**2 + (y3-y1)**2 - (r3+r2)**2


def floatRange(start, end=None, step=None):
    if start > end:
        raise ValueError
    if step != None and end == None:
        raise ValueError
    elif not end and not step:
        end = start
        start = 0.0
        step = 1.0
    elif end and not step:
        step = 1.0
    result = []
    while start < end:
        result.append(start)
        start += step
    return result
        


def equations(loc, r3, path):    
    x3, y3 = loc
    shape1 = path[-1]
    shape2 = path[-2]
    x1, y1 = shape1.getLoc()
    r1 = shape1.getRadius()
    x2, y2 = shape2.getLoc()
    r2 = shape2.getRadius()
    return ((x3-x1)**2 + (y3-y1)**2 - (r3+r1)**2, 
            (x3-x2)**2 + (y3-y2)**2 - (r3+r2)**2)


def getCenter(node2insert,rootNode, path=[]):
    if len(path) == 0:
        return 0,0
    elif len(path) == 1:
        r = path[0].getRadius()
        r3 = node2insert.getRadius()
        return -r-r3,0
    else:
        r3 = node2insert.getRadius()
        shape2 = path[-1]
        x1,y1 = rootNode.getLoc()
        r1 = rootNode.getRadius()
        x2,y2 = shape2.getLoc()
        # TODO
#        x,y =  fsolve(equations, (startX,startY), (r3, [shape1,shape2]))
#        return x,y
        for xx in floatRange(x1-r1-r3, x1+r1+r3+1, r1+r3/20.0):
            deltaY = sqrt(abs((r1+r3)**2 - (x1-xx)**2))
            for yy in [y1-deltaY,y1+deltaY]:
                print('(%.2f,%.2f)' % (xx,yy)),
                bol = True
                x,y =  fsolve(equations, (xx,yy), (r3, [rootNode,shape2]))
                print('(%.2f,%.2f)' % (x,y))
                for shape in path:
                    rx = shape.getRadius()
                    loc=shape.getLoc()
                    if rx+r3 > sqrt((x-loc[0])**2 + (y-loc[1])**2):
                        bol = False
                if bol:
                    print('Got: (%.2f,%.2f)' % (x,y))
                    return x,y
        return False, False                 
                




def calcCircle(x):
    r=1
    y = 1
    return (x**2 + y**2 - r**2)
    


def BFS(graph, path=[], result =[]):
    if len(graph) == 0:
        return result
    if not path:
        start = graph.pop(0)
        start.insertLoc(0,0)
        path = path + [start]
        result.append(start)
    for shape in path:
        for node2insert in shape.getNodes():
            if node2insert not in path and node2insert not in result:
                try:
                    x,y = getCenter(node2insert,shape, path)
                    node2insert.insertLoc(x,y)
                    result.append(node2insert)
                    path += [node2insert]
                    graph.remove(node2insert)                
                except TypeError:
                    print('Error') 
        path.remove(shape)
    return BFS(graph, path, result)
            
    
    



shapeList =[]
shapeAddedList = []


for n in range(150):
    a = Shape(str(n), pi*(random.randrange(1,3)**2))
    shapeList.append(a)  
    
#
for n in shapeList:
    n.addNode(random.sample(shapeList, 1))

root = None
nr = 0
for shape in shapeList:
    if len(shapeAddedList) == 0:
        root = shape
        x,y = 0,0
    elif len(shapeAddedList) == 1:
        r1 = shapeAddedList[-1].getRadius()
        r = shape.getRadius()
        x,y = -r-r1,0
    else:
        found = False
        while not found:
            x,y = getCenter(shape, root, shapeAddedList)
            if x == False or y == False:
                nr +=1
                root = shapeAddedList[nr]    
            else:
                found = True
                print('Current root: %d' % nr)
    shape.insertLoc(x,y)
    shapeAddedList.append(shape)

#shapeAddedList = BFS(shapeList)

maxR = 0
minX, maxX = True, 0
minY, maxY = True, 0

for n in shapeAddedList:
    if maxR < n.getRadius():
        maxR = n.getRadius()
    if minX > n.getLoc()[0]:
        minX = n.getLoc()[0]
    if minY > n.getLoc()[1]:
        minY = n.getLoc()[1]
    if maxX < n.getLoc()[0]:
        maxX = n.getLoc()[0]
    if maxY < n.getLoc()[1]:
        maxY = n.getLoc()[1]
        
        
print('\n\n')
print(maxR)
print(minX,maxX)
print(minY,maxY)


print('\nplotting')
fig = plt.gcf()
plt.ylim(int(minY-maxR*2), int(maxY+maxR*2))
plt.xlim(int(minX-maxR*2), int(maxX+maxR*2))
for shape in shapeAddedList:
    x,y = loc = shape.getLoc()
    r = shape.getRadius()
    col = (random.random(), random.random(), random.random())
    fig.gca().add_artist(plt.Circle(loc, r, fill = False, linewidth=.3, color=col))
    fig.gca().add_artist(plt.text(x,y,shape.getName(), color = col))
    
    
points = [s.getLoc() for s in shapeAddedList]    
vor = Voronoi(points)
vorplot = voronoi_plot_2d(vor)
    
fig.savefig('a.png')
fig.show()