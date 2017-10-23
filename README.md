Projekt "Hochregallager sortieren"

Problembeschreibung:
Ein Hochregallager mit n Lagerplätzen soll sortiert werden. Alle Lagerplätze bis
auf einen sind belegt. Dabei wird jedem Element eine Wertigkeit von 0 bis n-2
zugeordnet, dem leeren Feld der Wert Null. Ziel ist, dass jedes Element an der Position
liegt, deren Index seiner Wertigkeit entspricht. Der leere Lagerplatz ist dabei
der letzte bzw. n-1. Die Lagerplätze werden dabei von Null an fortlaufend nummeriert.

Es kann immer nur ein Element gleichzeitig transportiert werden und der einzige
mmögliche Ablageort ist der aktuell leere Lagerplatz.
Jede Bewegung benötigt Zeit zur Durchführung, abhängig vom Abstand der anzufahrenden
Plätze. Zur Berechnung dieser muss die Breite des Lagers bekannt sein.

Es soll versucht werden, den schnellsten Lösungsweg zu finden.

Analyse:
Jede Permutation einer Menge von Werten (entspr. Wertigkeit der Elemente) lässt
sich in Untermengen aufteilen, die untereinander vertauscht sind. Einige dieser Untermengen enthalten dabei nur einen Wert, diese Werte liegen schon an der
richtigen Position.

Die Mengen von Werten lassen sich in Ketten anordnen, die beschreiben, in 
welcher Reihenfolge diese Werte bewegt werden müssen, um an der korrekten
Position zu liegen. Im folgenden wird die Bezeichnung "Ketten" verwendet.

Die Ketten werden so sortiert, dass die Kette mit dem Wert Null an erster Stelle
liegt. Dabei ist Null das letzte Element der Kette. Die Ketten mit nur einem Wert
werden nicht weiter betrachtet. Jede Kette wird nacheinander betrachtet.

Enthält die erste Kette nun den Wert Null, kann diese Kette sofort sortiert werden.
Ist dies die einzige Kette, entspricht sie der schnellsten Lösung (Fall 1).

Jedes Element der Kette bis Null wird durchlaufen und die Kosten für die Bewegung
berechnet. Die Startposition muss festgelegt werden/bekannt sein.
Details, wie die Kosten berechnet werden und die nötigen Bewegungen aus den Ketten
bestimmt werden können siehe (noch) Kommentare im Code (krasser Voodoo).

Enthält die erste Kette nicht den Wert Null (Null war also an der richtigen Position
und in einer Kette der Länge 1) oder für alle folgenden Ketten kann nun
ein primitiver Lösungsweg verwendet werden (Fall 2):

Das Ende der Kette wird um das erste Element der Kette sowie den Wert Null ergänzt.
So ergibt sich eine sortierbare Kette. Alle Bewegungen werden zu einer einfachen
Lösungskette verbunden, die als Kostenfunktion verwendet wird.

Schnellste Lösung:
Um den schnellsten Lösungsweg zu finden, müssen alle Möglichkeiten betrachtet werden:
Es gibt folgende Bewegungs-Optionen:
1. Enthält die erste Kette None, dann das erste Element dieser Kette
2. + alle Elemente aus allen Ketten, die nicht None enthalten

Das ergibt eine Liste an Bewegungen und daraus resultierenden Permutationen,
die bei Aufaddierung der Kosten und Rückverfolgung der Pfade rekursiv durchlaufen
werden. Für jede Permutation werden die Ketten bestimmt. Gibt es keine Ketten
mit mehr als einem Element, ist ein Rekursionsausstieg erreicht. Die rekursiv
aufaddierten Kosten und der Pfad werden zurückgegeben.

Ein weiterer Rekursionsausstieg findet statt, wenn alle Bewegungs-Optionen
bereits im verfolgten Pfad enthalten sind. Dann wird die Kostenfunktion bestimmt
und zurückgegeben.

Funktioniert. Wow.