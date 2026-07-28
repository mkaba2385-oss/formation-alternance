notes = [12, 15, 8, 18, 10]
eleves = ["Alice", "Bob", "Charlie", "David", "Eva"]

resultats = [eleve for eleve, note in zip(eleves, notes) if note >= 10]

print("Élèves admis :")  
for eleve in resultats:    
    print(eleve)   

moyenne = sum(notes) / len(notes)  
print(f"Moyenne : {moyenne:.2f}")   

meilleur_eleve, meilleure = max(
    zip(eleves, notes),
    key=lambda x: x[1]
)

print(f"Meilleure note : {meilleure}")
print(f"Élève : {meilleur_eleve}")

for eleve, note in zip(eleves, notes):
    if note >= 10:
        print(f"{eleve} a réussi")
    else:
        print(f"{eleve} a échoué")