notes = [12, 15, 8, 18, 10]
eleves = ["Alice", "Bob", "Charlie", "David", "Eva"]

resultats = []

for i in range(len(notes)):
    if notes[i] >= 10:
        resultats.append(eleves[i])

print("Élèves admis :")
for i in range(len(resultats)):
    print(resultats[i])

total = 0
for i in range(len(notes)):
    total = total + notes[i]

moyenne = total / len(notes)
print("Moyenne :", moyenne)

meilleure = notes[0]
meilleur_eleve = eleves[0]

for i in range(len(notes)):
    if notes[i] > meilleure:
        meilleure = notes[i]
        meilleur_eleve = eleves[i]

print("Meilleure note :", meilleure)
print("Élève :", meilleur_eleve)

for i in range(len(eleves)):
    if (notes[i] >= 10) == True:
        print(eleves[i], "a réussi")
    else:
        print(eleves[i], "a échoué")