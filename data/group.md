# Grouping Genetic Algorithm (GGA) – Vorgehen und Beispiel

Der **Grouping Genetic Algorithm (GGA)** ist ein Ansatz aus der :contentReference[oaicite:0]{index=0} und wird für Optimierungsprobleme verwendet, bei denen nicht die Reihenfolge von Elementen entscheidend ist, sondern deren **Zugehörigkeit zu Gruppen (Clustern)**.

Typische Anwendungen sind Clusterprobleme, Ressourcenaufteilung oder Gruppenzuweisungen mit festen Gruppengrößen.

---

# 1. Theoretisches Vorgehen (Grouping-Ansatz)

Im Gegensatz zu permutationbasierten Verfahren (z. B. OX oder PMX) besteht ein Individuum im GGA aus **expliziten Gruppen**.

---

## 1.1 Repräsentation eines Individuums

Ein Individuum ist eine Partition der Menge aller Elemente in feste Gruppen:

- Jede Gruppe hat eine feste Größe (z. B. 20 Elemente)
- Jedes Element kommt genau einmal vor

Beispielstruktur:

Individuum =
[
  Gruppe 1 (Liga 1),
  Gruppe 2 (Liga 2),
  Gruppe 3 (Liga 3),
  Gruppe 4 (Liga 4)
]

---

## 1.2 Rekombination (Grouping Crossover)

Die Rekombination erfolgt nicht über Positionen, sondern über **Gruppenvererbung**:

### Ablauf:

1. Wähle zwei Elternindividuen
2. Übernehme zufällig einige komplette Gruppen von Parent 1
3. Übernehme weitere Gruppen von Parent 2
4. Prüfe auf doppelte oder fehlende Elemente
5. Führe eine **Reparaturphase (Repair)** durch:
   - entferne doppelte Elemente
   - füge fehlende Elemente in Gruppen ein
   - achte auf feste Gruppengröße

---

## 1.3 Mutation (typisch im GGA)

Mutation erfolgt meist durch:
- Austausch von Elementen zwischen Gruppen
- Verschieben einzelner Elemente
- lokale Umstrukturierung innerhalb einer Gruppe

---

## Eigenschaften

Der GGA stellt sicher, dass:

- jedes Element genau einer Gruppe zugeordnet ist
- Gruppengrößen eingehalten werden
- die Struktur der Cluster im Fokus steht (nicht Reihenfolge)

---

# 2. Beispiel für Grouping

## Gegeben: 8 Teams, 2 Ligen à 4 Teams

Teams:
{1, 2, 3, 4, 5, 6, 7, 8}

---

## Parent A

Liga 1: {1, 2, 3, 4}  
Liga 2: {5, 6, 7, 8}

---

## Parent B

Liga 1: {1, 5, 6, 7}  
Liga 2: {2, 3, 4, 8}

---

## Schritt 1: Gruppen auswählen

- von Parent A: Liga 1 wird übernommen
- von Parent B: Liga 2 wird übernommen

---

## Zwischenzustand (ohne Repair)

Liga 1: {1, 2, 3, 4}  
Liga 2: {2, 3, 4, 8}

---

## Problem

- Duplikate: {2, 3, 4}
- Fehlende Elemente: {5, 6, 7}

---

## Schritt 2: Repair

### Entferne Duplikate

Liga 1: {1, 2, 3, 4}  
Liga 2: {8, _, _, _}

### Füge fehlende Elemente ein

Fehlend: {5, 6, 7}

---

## Repariertes Ergebnis

Liga 1: {1, 2, 3, 4}  
Liga 2: {5, 6, 7, 8}

---

# 3. Übertragung auf dein Kompassmodell

Für dein Problem bedeutet das:

- 80 Teams
- 4 Ligen
- jede Liga genau 20 Teams

Ein Individuum ist:

[
  20 Teams (Liga 1),
  20 Teams (Liga 2),
  20 Teams (Liga 3),
  20 Teams (Liga 4)
]

---

## Zielfunktion (typisch)

Minimierung von:

- durchschnittlicher Reiseentfernung innerhalb jeder Liga
- oder Gesamtstrecke aller Ligaspiele

---

# 4. Zusammenfassung

Der Grouping Genetic Algorithm unterscheidet sich fundamental von permutationbasierten Ansätzen:

- Fokus liegt auf **Zugehörigkeit statt Reihenfolge**
- Crossover operiert auf **Gruppen statt Positionen**
- Reparatur ist essenziell zur Einhaltung der Constraints

---

# Merksatz

Beim Grouping GA ist nicht entscheidend, in welcher Reihenfolge Elemente stehen, sondern in welcher Gruppe sie sich befinden.



















# Konkretes Beispiel: Rekombination im Kompassmodell (80 Teams, 4 Ligen)

Wir betrachten eine sehr konkrete Rekombination zweier Individuen im evolutionären Algorithmus. Die Lösung ist als Permutation von 80 Teams dargestellt und wird anschließend strikt in 4 Ligen zu je 20 Teams aufgeteilt.

---

## Ausgangssituation

Wir haben zwei Elternlösungen (Parent A und Parent B), beide enthalten jeweils alle Teams von 1 bis 80 genau einmal, unterscheiden sich aber in der Reihenfolge.

Parent A ist strukturiert und entspricht bereits einer „geordneten“ Lösung:


Parent A:
[1, 2, 3, ..., 20, 21, 22, ..., 40, 41, 42, ..., 60, 61, 62, ..., 80]


Parent B ist stark durchmischt und erzeugt eine völlig andere Gruppierung:


Parent B:
[1, 21, 41, 61, 2, 22, 42, 62, 3, 23, 43, 63, ..., 20, 40, 60, 80]


---

## Rekombinationsverfahren (liga-basierter Crossover)

Für die Rekombination werden gezielt ganze Ligen von Parent A übernommen. Danach werden die verbleibenden Teams in der Reihenfolge von Parent B eingefügt, sodass eine gültige Permutation ohne Duplikate entsteht.

Wir wählen konkret:

- Liga 1 und Liga 3 von Parent A werden übernommen
- Liga 2 und Liga 4 werden aus Parent B ergänzt

---

## Schritt 1: Übernahme aus Parent A

Aus Parent A werden direkt folgende Blöcke übernommen:

Liga 1 (Position 1–20):

[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]


Liga 3 (Position 41–60):

[41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60]


Die bereits verwendeten Teams sind damit:
1–20 und 41–60.

---

## Schritt 2: Filterung von Parent B

Nun wird Parent B durchlaufen und alle bereits verwendeten Teams (1–20 und 41–60) entfernt. Übrig bleiben exakt die Teams:


[21, 61, 22, 62, 23, 63, 24, 64, 25, 65, 26, 66, 27, 67, 28, 68, 29, 69, 30, 70,
31, 71, 32, 72, 33, 73, 34, 74, 35, 75, 36, 76, 37, 77, 38, 78, 39, 79, 40, 80]


---

## Schritt 3: Aufbau der verbleibenden Ligen

Diese gefilterte Liste wird nun sequenziell in die offenen Ligen eingefügt.

---

### Liga 2 (20 Teams aus gefiltertem Parent B)


[21, 61, 22, 62, 23, 63, 24, 64, 25, 65, 26, 66, 27, 67, 28, 68, 29, 69, 30, 70]


---

### Liga 4 (restliche 20 Teams aus gefiltertem Parent B)


[31, 71, 32, 72, 33, 73, 34, 74, 35, 75, 36, 76, 37, 77, 38, 78, 39, 79, 40, 80]


---

## Ergebnis (vollständiges Kind)

Nach der Rekombination ergibt sich exakt folgende neue Lösung:

Liga 1:

[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]


Liga 2:

[21, 61, 22, 62, 23, 63, 24, 64, 25, 65, 26, 66, 27, 67, 28, 68, 29, 69, 30, 70]


Liga 3:

[41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60]


Liga 4:

[31, 71, 32, 72, 33, 73, 34, 74, 35, 75, 36, 76, 37, 77, 38, 78, 39, 79, 40, 80]


---

## Interpretation

Diese Rekombination kombiniert zwei Eigenschaften:

- stabile, geordnete Ligen aus Parent A (Liga 1 und 3)
- stark explorative Durchmischung aus Parent B (Liga 2 und 4)

Damit entsteht eine neue Lösung, die sowohl Struktur erhält als auch neue Kombinationen ermöglicht, ohne die Permutationsbedingungen zu verletzen.
