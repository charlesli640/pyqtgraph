# -*- coding: utf-8 -*-
"""
Simple example of subclassing GraphItem.
"""

import initExample ## Add path to library (just for examples; you do not need this)
import random
from time import sleep

import socket
import threading
import traceback
import zmq
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

values = None

class ChannelSubThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.running = False
        #self.context = zmq.Context()
        #self.sock = self.context.socket(zmq.SUB)
        #self.sock.setsockopt_string(zmq.SUBSCRIBE, '')
        #self.addr = "tcp://localhost:6789"


    def stop(self):
        self.running = False
        #self.sock.disconnect(self.addr)
        #self.sock.close()

    def run(self):
        global values
        host = 'localhost'
        port = 6789

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        self.running = True
        #self.sock.connect(self.addr)
        # loop
        while self.running:
            #message = s.recv()
            try:
                message, address = s.recvfrom(8192)
                #print("Got data from {} : {}".format(address, message))
                values = np.frombuffer(message, dtype=np.ubyte)
            except (KeyboardInterrupt, SystemExit):
                raise
            except:
                traceback.print_exc()
            payload0 = "{}:{}".format("tcp ", time())
            #print("{} recv len={}".format(payload0, len(message)))
            #sleep(0.05)

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
    #clrs = np.random.rand(N)
    global values
    clrs = np.random.rand(N)
    if values is not None and np.prod(values.shape) > 0:
        clrs = values.copy().astype(np.float)
        clrs.resize(N)
        clrs *= 1.0/255.0
        #print("{:.2f} {:.2f} {:.2f} {:.2f} {:.2f}".format(clrs[0], clrs[1], clrs[2], clrs[3], clrs[4]))
        #print("clr={}".format(clrs))
    #clrs = clrs*255
    #clrs = clrs.astype(dtype=np.ubyte)
    t1 = time()
    g.setData(pos=pos, size=4, pxMode=False, symbol='s', symbolBrush=clrs)

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

    #print("t0={} t1={} t2={}".format(t0, t1, now))

#update()
timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(0)


## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        sub = ChannelSubThread()
        sub.start()
        QtGui.QApplication.instance().exec_()

        sub.stop()
        sub.join()
