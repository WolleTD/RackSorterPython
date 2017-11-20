#!/usr/bin/env python

import racksorter
import pyads
import time
from copy import copy


xSize = 3;
ySize = 3;
    

def index2ADS(n):
    xPos = n % xSize
    yPos = 3 - (n // ySize)
    return (xPos << 8) + yPos


def waitForAdsWrite(plc, group, offset, value, plctype):
    while not plc.read_write(group, offset, pyads.PLCTYPE_BOOL, value, plctype):
        time.sleep(0.05)
    

def adsControl(data, solution):
    plc = pyads.Connection('127.0.0.1.1.1', pyads.PORT_SPS1)
    plc.open()
    plc.read_write(1, 1, pyads.PLCTYPE_BOOL, True, pyads.PLCTYPE_BOOL)
    
    for element in solution:
        valueIndex = data.index(element)
        noneIndex = data.index(None)
        
        valuePos = index2ADS(valueIndex)
        nonePos = index2ADS(noneIndex)
        waitForAdsWrite(plc, 2, 1, valuePos, pyads.PLCTYPE_UINT)
        waitForAdsWrite(plc, 2, 3, True, pyads.PLCTYPE_BOOL)
        waitForAdsWrite(plc, 2, 2, nonePos, pyads.PLCTYPE_UINT)
        waitForAdsWrite(plc, 2, 4, True, pyads.PLCTYPE_BOOL)
        
        data[noneIndex], data[valueIndex] = element, None
    plc.close()


def main():
    racksorter.setDimensions(3, 3)
    inputArray = [4, 3, 7, 0, 1, 6, None, 2, 5]
    solution = racksorter.findShortestPath(inputArray)
    adsControl(copy(inputArray), solution)


if __name__ == '__main__':
    main()
