# Grouping Genetic Algorithm (GGA) – Vorgehen und Beispiel

Der **Grouping Genetic Algorithm (GGA)** ist ein Ansatz aus der :contentReference[oaicite:0]{index=0} und wird für Optimierungsprobleme verwendet, bei denen nicht die Reihenfolge von Elementen entscheidend ist, sondern deren **Zugehörigkeit zu Gruppen (Clustern)**.

Typische Anwendungen sind Clusterprobleme, Ressourcenaufteilung oder Gruppenzuweisungen mit festen Gruppengrößen.

---

# 🧠 1. Theoretisches Vorgehen (Grouping-Ansatz)

Im Gegensatz zu permutationbasierten Verfahren (z. B. OX oder PMX) besteht ein Individuum im GGA aus **expliziten Gruppen**.

---

## 🧬 1.1 Repräsentation eines Individuums

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

## 🔁 1.2 Rekombination (Grouping Crossover)

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

## 🔧 1.3 Mutation (typisch im GGA)

Mutation erfolgt meist durch:
- Austausch von Elementen zwischen Gruppen
- Verschieben einzelner Elemente
- lokale Umstrukturierung innerhalb einer Gruppe

---

## 📌 Eigenschaften

Der GGA stellt sicher, dass:

- jedes Element genau einer Gruppe zugeordnet ist
- Gruppengrößen eingehalten werden
- die Struktur der Cluster im Fokus steht (nicht Reihenfolge)

---

# 🧪 2. Beispiel für Grouping

## 🔹 Gegeben: 8 Teams, 2 Ligen à 4 Teams

Teams:
{1, 2, 3, 4, 5, 6, 7, 8}

---

## 🔹 Parent A

Liga 1: {1, 2, 3, 4}  
Liga 2: {5, 6, 7, 8}

---

## 🔹 Parent B

Liga 1: {1, 5, 6, 7}  
Liga 2: {2, 3, 4, 8}

---

## 🔁 Schritt 1: Gruppen auswählen

- von Parent A: Liga 1 wird übernommen
- von Parent B: Liga 2 wird übernommen

---

## 🔹 Zwischenzustand (ohne Repair)

Liga 1: {1, 2, 3, 4}  
Liga 2: {2, 3, 4, 8}

---

## ⚠️ Problem

- Duplikate: {2, 3, 4}
- Fehlende Elemente: {5, 6, 7}

---

## 🔧 Schritt 2: Repair

### Entferne Duplikate

Liga 1: {1, 2, 3, 4}  
Liga 2: {8, _, _, _}

### Füge fehlende Elemente ein

Fehlend: {5, 6, 7}

---

## 🔹 Repariertes Ergebnis

Liga 1: {1, 2, 3, 4}  
Liga 2: {5, 6, 7, 8}

---

# 🏟️ 3. Übertragung auf dein Kompassmodell

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

## 🎯 Zielfunktion (typisch)

Minimierung von:

- durchschnittlicher Reiseentfernung innerhalb jeder Liga
- oder Gesamtstrecke aller Ligaspiele

---

# 📌 4. Zusammenfassung

Der Grouping Genetic Algorithm unterscheidet sich fundamental von permutationbasierten Ansätzen:

- Fokus liegt auf **Zugehörigkeit statt Reihenfolge**
- Crossover operiert auf **Gruppen statt Positionen**
- Reparatur ist essenziell zur Einhaltung der Constraints

---

# 🧠 Merksatz

> Beim Grouping GA ist nicht entscheidend, in welcher Reihenfolge Elemente stehen, sondern in welcher Gruppe sie sich befinden.