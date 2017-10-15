Projekt "Hochregallager sortieren"



https://github.com/DaveDinaro/HighRackWarehouse_Runtime

Eingabe:

Zweidimensionales Array im Prinzip überflüssig wenn
Parameter "Regalbreite" gegeben.
Dann Eingabe Array/Liste mit Länge n_Regalbreite*n_Regalhöhe,
Index 0 oben links, index n_Regalbreite 2. Reihe v.o. links usw
```
1. Stufe: Regal 3x3, Array-Länge 9
2. Stufe: n*m
```
Array-Inhalt:
```
1. Stufe: int 0-7 und None/NULL
2. Stufe: int 0-8 und None/NULL
3. Stufe: Alle Sortables und None/NULL
```
Voraussetzung:
```
1. Stufe: Alle Werte 0-7 und 1x None/NULL im Array
2. Stufe: 8 Werte aus 0-8 und 1x None/NULL
3. Stufe: Alle Sortables und 1x None/NULL
4. Stufe: Alle Sortables und *x None/NULL
```
Jeweils zufällig verteilt/unsortiert

Ziel:
```
1. Stufe: Werte 0-7 bei jeweiligem Index, None bei 8
2. Stufe: Werte aus 0-8 bei jeweiligem Index, None bei unbelegtem Index
3. Stufe: ?
```

Ablaufbeispiel:
```
Eingabe: 5 1 3 7 6 _ 4 2 0
Ziel:    0 1 2 3 4 5 6 7 _
```

Das Feld wird in untereinander vertauschte Gruppen aufgeteilt:
```
1, 6->4, 0->5->_. 3->2->7
```

Die Gruppe startet mit dem ersten Index, gefolgt vom Wert an dieser Stelle. Dann wird der Wert als Index gewählt und der Wert an dieser Stelle angehängt, sofern er nicht dem Index entspricht, mit dem die Gruppe startet. Dann ist sie vollständig und eine neue Gruppe startet mit dem ersten Index, der noch nicht einer Gruppe zugeordnet ist.
