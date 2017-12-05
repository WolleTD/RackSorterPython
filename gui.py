# -*- coding: utf-8 -*-

import sys
from collections import namedtuple, Counter
import PyQt5.QtCore as core
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

racksorter.setDimensions(config.xSize, config.ySize)
app = widgets.QApplication(sys.argv)
window = uic.loadUi("main.ui")


def initConfigUI():
    window.sbWidth.setValue(config.xSize)
    window.sbHeight.setValue(config.ySize)
    window.leTCAddr.setText(config.adsAddr)
    window.leTCPort.setText(str(config.adsPort))
    

def makeGrid(box, readOnly = False):
    for w in [c for c in box.children() if type(c) is widgets.QWidget]:
        w.setParent(None)
    layout = box.layout()
    positions = [(i,j) for i in range(config.ySize) for j in range(config.xSize)]
    
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


def gridToList(box):
    l = []
    layout = box.layout()
    positions = [(i,j) for i in range(config.ySize) for j in range(config.xSize)]
    for idx in range(len(positions)):
        p = positions[idx]
        w = layout.itemAtPosition(*p).widget()
        v = w.children()[2].value()
        # Convert to racksorter indexes
        v = v - 1 if v != 0 else None
        l.append(v)
    nonUniq = [k for (k, v) in Counter(l).items() if v > 1]
    for idx in range(len(positions)):
        p = positions[idx]
        w = layout.itemAtPosition(*p).widget()
        v = w.children()[2].value()
        v = v - 1 if v != 0 else None
        if v in nonUniq:
            w.setStyleSheet('QWidget{background-color:#fea0a0}')
        else:
            w.setStyleSheet('')
    if len(nonUniq) == 0:
        return l
    else:
        return None


def listToGrid(box, l):
    lView = [0 if i is None else i + 1 for i in l]
    layout = box.layout()
    positions = [(i,j) for i in range(config.ySize) for j in range(config.xSize)]
    for idx in range(len(positions)):
        p = positions[idx]
        layout.itemAtPosition(*p).widget().children()[2].setValue(lView[idx])
        

def simulationIteration(data, idx, path, positions, prevIdx = -1):
    layout = window.gbState.layout()
    element = path[idx]
    valueIndex = data.index(element)
    noneIndex = data.index(None)
    print("Moving {} from {} to {}".format(element, positions[valueIndex], positions[noneIndex]))
    window.teInfo.setText("Moving {} from {} to {}".format(element, positions[valueIndex], positions[noneIndex]))
    prevWidget = layout.itemAtPosition(*positions[prevIdx]).widget()
    valueWidget = layout.itemAtPosition(*positions[valueIndex]).widget()
    noneWidget = layout.itemAtPosition(*positions[noneIndex]).widget()
    valueWidget.setStyleSheet('QWidget{background-color:#ef8888}')
    noneWidget.setStyleSheet('QWidget{background-color:#efef88}')
    if prevIdx == path[idx - 1]:
        prevWidget.setStyleSheet('QWidget{background-color:#88ef88}')
    else:
        prevWidget.setStyleSheet('')
    listToGrid(window.gbState, data)
    data[noneIndex], data[valueIndex] = element, None
    if element is not None:
        core.QTimer.singleShot(1000, lambda: simulationIteration(data, idx + 1, path, positions, noneIndex))
    else:
        core.QTimer.singleShot(1000, lambda: noneWidget.setStyleSheet('QWidget{background-color:#88ef88}'))


def solutionButtonClick():
    l = gridToList(window.gbInput)
    if l is None:
        window.teInfo.setText("All elements have to be unique!")
        return False
    sp = racksorter.findShortestPath(l)
    window.teInfo.setText("Shortest Path with {} steps:\n{}".format(sp[1], ['_' if i is None else i + 1 for i in sp[0]]))


def simulationButtonClick():
    data = gridToList(window.gbInput)
    print("Read data:", data)
    positions = [(i,j) for i in range(config.ySize) for j in range(config.xSize)]
    if data is None:
        window.teInfo.setText("All elements have to be unique!")
        return False
    listToGrid(window.gbState, data)
    for w in [n for n in window.gbState.children() if type(n) is widgets.QWidget]:
        w.setStyleSheet('')
    path = racksorter.findShortestPath(data)[0]
    core.QTimer.singleShot(1000, lambda: simulationIteration(data, 0, path, positions))
 

def setConfigButtonClick():
    global config
    config = Config(xSize = window.sbWidth.value(),
                ySize = window.sbHeight.value(),
                adsAddr = window.leTCAddr.text(),
                adsPort = int(window.leTCPort.text()))
    makeGrid(window.gbInput)
    makeGrid(window.gbState, True)
    racksorter.setDimensions(config.xSize, config.ySize)
    

def main():
    # Main Program
    initConfigUI()
    makeGrid(window.gbInput)
    makeGrid(window.gbState, True)
    window.btnFindSolution.clicked.connect(solutionButtonClick)
    window.btnSimulation.clicked.connect(simulationButtonClick)
    window.btnSetConfig.clicked.connect(setConfigButtonClick)
    
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()
