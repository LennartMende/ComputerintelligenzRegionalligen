# Workflow für die Rekombination nach dem Order Crossover (OX)

Der **Order Crossover (OX)** ist ein Rekombinationsoperator, der speziell für Probleme mit **Permutationscodierung** entwickelt wurde. Typische Anwendungsfelder sind Routing-, Scheduling- und Zuordnungsprobleme, bei denen jedes Element genau einmal vorkommen darf.

---

# Theoretischer Ablauf des Order Crossover (OX)

Gegeben sind zwei Elternindividuen gleicher Länge \( L \), die jeweils eine Permutation darstellen.

Der OX-Operator erzeugt ein Kindindividuum in vier Schritten:

---

## 1. Auswahl eines Substrings

Zunächst werden zwei zufällige Crossover-Punkte \( i \) und \( j \) (mit \( i < j \)) bestimmt.

Das Intervall \([i, j]\) definiert ein zusammenhängendes Segment in **Parent 1**.

---

## 2. Kopieren des Segments

Das ausgewählte Segment aus Parent 1 wird **unverändert und positionsgetreu** in das Kind übernommen.

Alle übrigen Positionen bleiben zunächst leer.

---

## 3. Extraktion der restlichen Gene

Nun werden die Elemente von **Parent 2** betrachtet.

Dabei gilt:
- Es werden alle Gene aus Parent 2 in ihrer Reihenfolge durchlaufen
- Gene, die bereits im Kind vorhanden sind (aus Schritt 2), werden übersprungen

---

## 4. Einfügen mit Wrap-Around

Die verbleibenden Gene aus Parent 2 werden in die freien Positionen des Kindes eingefügt.

Dabei wird:
- von links nach rechts aufgefüllt
- am Ende der Liste wieder am Anfang fortgesetzt (Wrap-Around)
- die ursprüngliche Reihenfolge von Parent 2 beibehalten

---

## Eigenschaften

Der OX-Operator stellt sicher, dass:
- jede Permutation gültig bleibt (keine Duplikate entstehen)
- ein zusammenhängender Teil von Parent 1 erhalten bleibt
- die relative Reihenfolge von Parent 2 teilweise übernommen wird

---

# 2. Beispiel für den Order Crossover (OX)

## Gegebene Eltern

Wir betrachten zwei Elternchromosomen:

**Parent 1:**

1 2 3 4 5 6 7 8


**Parent 2:**

4 1 2 8 7 6 5 3


---

## Schritt 1: Crossover-Punkte wählen

Wir wählen beispielhaft:

- \( i = 3 \)
- \( j = 5 \)

---

## Schritt 2: Segment aus Parent 1 kopieren

Das Segment von Position 3 bis 5 aus Parent 1 lautet:


3 4 5


Das Kind sieht zunächst so aus:


_ _ 3 4 5 _ _ _


---

## Schritt 3: Parent 2 verarbeiten

Wir gehen Parent 2 der Reihe nach durch:


4 1 2 8 7 6 5 3


Bereits enthaltene Gene im Kind: `{3, 4, 5}` → werden übersprungen.

Verbleibende Reihenfolge:

1 2 8 7 6


---

## Schritt 4: Auffüllen (Wrap-Around)

Die freien Positionen werden von links nach rechts gefüllt:

Startzustand:

_ _ 3 4 5 _ _ _


Einfügen der restlichen Gene:

1 2 3 4 5 8 7 6


---

## Ergebnis (Kind)


1 2 3 4 5 8 7 6


Um aus 2 Eltern auch 2 Kinder zu erzeugen, wird derselbe Vorgang wiederholt, aber als Ausgangspunkt Parent 2 genommen und mit Parent 1 aufgefüllt.
