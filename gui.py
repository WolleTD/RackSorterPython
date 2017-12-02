# -*- coding: utf-8 -*-

import sys
from collections import namedtuple
import PyQt5.QtWidgets as widgets
import PyQt5.QtGui as gui
import PyQt5.uic as uic
import racksorter
import pyads


Config = namedtuple('Config', ['xSize', 'ySize', 'adsAddr', 'adsPort'])

config = Config(xSize = 3,
                ySize = 3,
                adsAddr = '127.0.0.1.1.1',
                adsPort = pyads.PORT_SPS1)

app = widgets.QApplication(sys.argv)
window = uic.loadUi("main.ui")


def initConfigUI():
    global config
    window.leWidth.setText(str(config.xSize))
    window.leHeight.setText(str(config.ySize))
    window.leTCAddr.setText(config.adsAddr)
    window.leTCPort.setText(str(config.adsPort))
    

def makeGrid(box, readOnly = False):
    global config
    layout = box.layout()
    positions = [(i,j) for i in range(config.xSize) for j in range(config.ySize)]
    
    for idx in range(len(positions)):
        p = positions[idx]
        # Creating QWidget and its layout
        w = widgets.QWidget(box)
        wlayout = widgets.QVBoxLayout()
        w.setLayout(wlayout)
        # Creating the label
        l = widgets.QLabel(w)
        l.setText("Fach {}:".format(idx + 1))
        # Font takes three lines -.-
        f = gui.QFont(l.font())
        f.setPointSize(12)
        l.setFont(f)
        wlayout.addWidget(l)
        # Creating the Spinner
        s = widgets.QSpinBox(w)
        s.setMaximum(len(positions) - 1)
        s.setSpecialValueText("_")
        s.setValue((idx + 1) % len(positions))
        s.setWrapping(True)
        # Read Only is different
        if readOnly:
            s.setReadOnly(readOnly)
            s.setButtonSymbols(widgets.QSpinBox.NoButtons)
            s.setValue(0)
        # Font
        f = gui.QFont(s.font())
        f.setPointSize(21)
        s.setFont(f)
        wlayout.addWidget(s)
        # Add widget to grid layout of group box
        layout.addWidget(w, *p)


def solutionButtonClick():
    global config
    l = []
    layout = window.gbInput.layout()
    positions = [(i,j) for i in range(config.xSize) for j in range(config.ySize)]
    for idx in range(len(positions)):
        p = positions[idx]
        v = layout.itemAtPosition(*p).widget().children()[2].value()
        # Convert to racksorter indexes
        v = v - 1 if v != 0 else None
        if v not in l:
            l.append(v)
        else:
            window.teInfo.setText("Nope.")
            return False
        
    window.teInfo.setText(str(l))
    sp = racksorter.findShortestPath(l)
    window.teInfo.setText("Shortest Path with {} steps:\n{}".format(sp[1], str(sp[0])))

# Main Program
initConfigUI()
makeGrid(window.gbInput)
makeGrid(window.gbState, True)
window.btnFindSolution.clicked.connect(solutionButtonClick)

window.show()
app.exec_()