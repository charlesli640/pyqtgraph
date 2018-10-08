# -*- coding: utf-8 -*-
"""
Simple example of subclassing GraphItem.
"""

import initExample ## Add path to library (just for examples; you do not need this)
import random
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
from pyqtgraph.ptime import time
import numpy as np

# Enable antialiasing for prettier plots
pg.setConfigOptions(antialias=True)

w = pg.GraphicsLayoutWidget(show=True)
w.setWindowTitle('pyqtgraph example: CustomGraphItem')
v = w.addViewBox()
v.setAspectLocked()

class Graph(pg.GraphItem):
    def __init__(self):
        self.dragPoint = None
        self.dragOffset = None
        self.textItems = []
        pg.GraphItem.__init__(self)
        self.scatter.sigClicked.connect(self.clicked)
        
    def setData(self, **kwds):
        self.text = kwds.pop('text', [])
        self.data = kwds
        if 'pos' in self.data:
            npts = self.data['pos'].shape[0]
            self.data['data'] = np.empty(npts, dtype=[('index', int)])
            self.data['data']['index'] = np.arange(npts)
        self.setTexts(self.text)
        self.updateGraph()
        
    def setTexts(self, text):
        for i in self.textItems:
            i.scene().removeItem(i)
        self.textItems = []
        for t in text:
            item = pg.TextItem(t)
            self.textItems.append(item)
            item.setParentItem(self)
        
    def updateGraph(self):
        pg.GraphItem.setData(self, **self.data)
        for i,item in enumerate(self.textItems):
            item.setPos(*self.data['pos'][i])
        
        
    def mouseDragEvent(self, ev):
        if ev.button() != QtCore.Qt.LeftButton:
            ev.ignore()
            return
        
        if ev.isStart():
            # We are already one step into the drag.
            # Find the point(s) at the mouse cursor when the button was first 
            # pressed:
            pos = ev.buttonDownPos()
            pts = self.scatter.pointsAt(pos)
            if len(pts) == 0:
                ev.ignore()
                return
            self.dragPoint = pts[0]
            ind = pts[0].data()[0]
            self.dragOffset = self.data['pos'][ind] - pos
        elif ev.isFinish():
            self.dragPoint = None
            return
        else:
            if self.dragPoint is None:
                ev.ignore()
                return
        
        ind = self.dragPoint.data()[0]
        self.data['pos'][ind] = ev.pos() + self.dragOffset
        self.updateGraph()
        ev.accept()
        
    def clicked(self, pts):
        print("clicked: %s" % pts)


g = Graph()
v.addItem(g)

textFps = pg.TextItem(html='<div style="text-align: center"><span style="color: #FFF;">This is the</span><br><span style="color: #FF0; font-size: 16pt;">Project 某某项目 </span></div>', anchor=(-0.3,0.5), angle=0, border='w', fill=(0, 0, 255, 100))
v.addItem(textFps)

## Update the graph
#g.setData(pos=pos, adj=adj, pen=lines, size=1, symbol=symbols, pxMode=False, text=texts)
fps = None
lastTime = time()

posa = []
C=30
R=30
N = C*R
## Define positions of nodes
for i in range(R):
    for j in range(C):
        p = [i*5, j*5]
        posa.append(p)

pos = np.array(posa, dtype=float)
textFps.setPos(0, 5*R+30)

def update():
    global g, pos, textFps, fps, lastTime
    
    ## Define the symbol to use for each node (this is optional)
    #symbols = ['o','o','o','o','t','+']
    
    ## Define the line style for each connection (this is optional)
    #lines = np.array([
    #    (255,0,0,255,1),
    #    (255,0,255,255,2),
    #    (255,0,255,255,3),
    #    (255,255,0,255,2),
    #    (255,0,0,255,1),
    #    (255,255,255,255,4),
    #    ], dtype=[('red',np.ubyte),('green',np.ubyte),('blue',np.ubyte),('alpha',np.ubyte),('width',float)])

    ## Define text to show next to each symbol
    #texts = ["Point %d" % i for i in range(N)]

    #colors=[]
    #for i in range(N):
        #c = random.uniform(0, 1) # (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    #    c = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    #    colors.append(c)
    t0 = time()
    clrs = np.random.rand(N)
    #clrs = clrs*255
    #clrs = clrs.astype(dtype=np.ubyte)
    t1 = time()
    g.setData(pos=pos, size=1, pxMode=False, symbol='o', symbolBrush=clrs)

    now = time()
    dt = now - lastTime
    lastTime = now
    if fps is None:
        fps = 1.0/dt
    else:
        s = np.clip(dt*3., 0, 1)
        fps = fps * (1-s) + (1.0/dt) * s

    html='<div style="text-align: center"><span style="color: #FFF;">This is the</span><br><span style="color: #FF0; font-size: 16pt;">Project 某某项目 {:.2f}</span></div>'.format(fps)
    textFps.setHtml(html)

    print("t0={} t1={} t2={}".format(t0, t1, now))

#update()
timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(0)


## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
