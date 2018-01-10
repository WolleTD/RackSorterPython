#!/usr/bin/env python

# file: adsClientRackSorter.py
#
# Kleines, statisches Testprogramm für die ADS-Kommunikation mit pyADS
# Eingabe-Daten für das racksorter-Modul sind direkt im Code in main()
# eingetragen.

import racksorter
import pyads
import time
from copy import copy

# Dimensionen des Hochregallagers
xSize = 3;
ySize = 3;
    
# Konvertiert einen list-Index zu Regal-Koordinaten
# im ADS Format (High Byte: xPos, Low Byte: yPos)
def index2ADS(n):
    xPos = n % xSize
    yPos = 3 - (n // ySize)
    return (xPos << 8) + yPos

# Versucht so lange wiederholt, einen ADS-Befehl auszuführen
# bis es funktioniert.
def waitForAdsWrite(plc, group, offset, value, plctype):
    while plc.read_write(group, offset, pyads.PLCTYPE_BOOL, value, plctype) != 0:
        time.sleep(0.05)
    
# Übersetzungs-Logik um die Lösung des racksorter-Moduls auf dem
# System auszuführen
def adsControl(data, solution):
    # ADS-Verbindung
    plc = pyads.Connection('127.0.0.1.1.1', pyads.PORT_SPS1)
    plc.open()
    plc.read_write(1, 1, pyads.PLCTYPE_BOOL, True, pyads.PLCTYPE_BOOL)
    # Lösung verarbeiten
    for element in solution:
        # Position des zu verschiebenden Elements
        valueIndex = data.index(element)
        # Position des leeren Felds
        noneIndex = data.index(None)
        # Zu ADS-Regal-Koordinaten konvertieren
        valuePos = index2ADS(valueIndex)
        nonePos = index2ADS(noneIndex)

        # Zur Beladen-Position fahren
        waitForAdsWrite(plc, 2, 1, valuePos, pyads.PLCTYPE_UINT)
        # Beladen
        waitForAdsWrite(plc, 2, 3, True, pyads.PLCTYPE_BOOL)
        # Zur Entladen-Position fahren (leeres Feld)
        waitForAdsWrite(plc, 2, 2, nonePos, pyads.PLCTYPE_UINT)
        # Entladen
        waitForAdsWrite(plc, 2, 4, True, pyads.PLCTYPE_BOOL)
        
        # "Virtuelles Regal" aktualisieren
        data[noneIndex], data[valueIndex] = element, None
    
    # Am Ende ADS-Verbindung schließen
    plc.close()

# Führt einen einfachen Test der ADS-Kommunikation mit
# einer racksorter-Lösung durch
def main():
    racksorter.setDimensions(xSize, ySize)
    
    # Eingabe für racksorter kann hier angepasst werden
    inputArray = [7, 3, None, 0, 1, 6, 5, 4, 2]
    
    solution = racksorter.findShortestPath(inputArray)[0]
    adsControl(copy(inputArray), solution)

# ifmain
if __name__ == '__main__':
    main()
