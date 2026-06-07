# PMX-Rekombinations-Algorithmus
Man hat 2 Parents parent1 und parent2 und erstellt daraus die Kinder offspring1 und offspring2.  
Dafür sucht man sich innerhalb der Listen zufällig einen Startpunkt und einen Endpunkt. Zwischen diesen beiden Punkten erhält offspring1 die Allele aus parent1.  
Außerhalb dieser Sequenz versucht man, offspring1 die Allele aus parent2 zuzuweisen und offspring2 die Allele aus parent1. Wenn aber Allele schon besetzt sind, muss man ein Mapping durchführen, da alle Teams in jedem Individuum genau einmal vorkommen müssen (Permutation).  
Ein geeignetes Beispiel ist dieses:  
P1 = [1 2 |3 4 5 6| 7 8]  
P2 = [5 7 |2 1 8 4| 3 6]  
Innerhalb des markierten Bereichs erfolgt parent1 -> offspring1 bzw. parent2 -> offspring2. Das Problem ist, dass man jetzt nicht für die restlichen Allele parent1 -> offspring2 bzw. parent2 -> offspring1 betreiben kann. Bspw. die 5 aus P2 kann nicht in O1 übernommen werden, da dort die 5 bereits vorhanden ist. Daher wird ein Mapping erstellt, wo jedem Punkt aus P1, der O1 zugeordnet wird, jeder Punkt aus P2, der in O2 geschrieben wird, zugeordnet wird.
P1 | 3 4 5 6  
------------  
P2 | 2 1 8 4  
Somit kann Punkt 5 aus P1 die 1 aus P2 zugeordnet werden, die auch noch nicht in O1 vorkommt.  