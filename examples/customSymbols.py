# -*- coding: utf-8 -*-
import initExample

from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
from pyqtgraph import functions as fn


app = QtGui.QApplication([])

mw = QtGui.QMainWindow()
view = pg.GraphicsLayoutWidget()  ## GraphicsView with GraphicsLayout inserted by default
mw.setCentralWidget(view)
mw.show()
mw.setWindowTitle('pyqtgraph example: ScatterPlot')
#w = view.addPlot()
w = view.addViewBox()
w.setAspectLocked()
#w.invertY(True)

#mysymbol = QtGui.QPainterPath()
#mysymbol.addText(0.0, 0.0, QtGui.QFont("San Serif", 1), "Y")
mysymbol = QtGui.QPainterPath()
mysymbol.addRect(0, 0, 5, 5)
#mysymbol.addText(0, 0, QtGui.QFont("San Serif", 5), 'Yes')
br = mysymbol.boundingRect()
scale = min(1. / br.width(), 1. / br.height())
tr = QtGui.QTransform()
tr.scale(scale, scale)
#tr.translate(-br.x() - br.width(), -br.y() - br.height())
mysymbol = tr.map(mysymbol)


s = pg.ScatterPlotItem(pxMode=False)   ## Set pxMode=False to allow spots to transform with the view
spots = []
for i in range(10):
    for j in range(20):
        spots.append({'pos': (i*10, j*10), 'size': 5, 'pen': fn.mkPen({'color': 'w', 'width': 1}),
        'brush':pg.intColor(i*10+j, 100), 'symbol': mysymbol})
s.addPoints(spots)
w.addItem(s)

mytext = QtGui.QPainterPath()
mytext.addText(0, 0, QtGui.QFont("San Serif", 15), 'Yes')
br = mytext.boundingRect()
scale = min(1. / br.width(), 1. / br.height())
tr = QtGui.QTransform()
tr.scale(scale, scale)
#tr.translate(-br.x() - br.width(), -br.y() - br.height())
mytext = tr.map(mytext)

t = pg.ScatterPlotItem(pxMode=True)
spott = []
for i in range(10):
    for j in range(20):
        spott.append({'pos': (i*10, j*10+5), 'size': 15, 'pen': fn.mkPen({'color': 'w', 'width': 2}),
        'brush':pg.intColor(i*10+j, 100), 'symbol': mytext})
t.addPoints(spott)
w.addItem(t)

text = pg.TextItem(html='<div style="text-align: center"><span style="color: #FFF;">This is the</span><br><span style="color: #FF0; font-size: 16pt;">Project 某某项目 </span></div>', anchor=(-0.3,0.5), angle=0, border='w', fill=(0, 0, 255, 100))
text.setPos(0, 220)
w.addItem(text)

if __name__ == '__main__':
    QtGui.QApplication.instance().exec_()
