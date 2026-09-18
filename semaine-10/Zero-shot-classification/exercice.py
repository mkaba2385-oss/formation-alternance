from transformers import pipeline
from sklearn.metrics import accuracy_score

classifier = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli"
)

texts = [
    "Le restaurant est excellent, la nourriture est délicieuse.",
    "Le service était très lent et le repas froid.",
    "Très bon restaurant, je reviendrai.",
    "Je suis déçu, la nourriture était mauvaise.",
    "Le serveur était sympathique et rapide.",
    "Prix trop élevé pour la qualité proposée.",
    "Excellent rapport qualité-prix.",
    "Je déconseille ce restaurant.",
    "La nourriture était correcte mais sans plus.",
    "Une expérience incroyable, tout était parfait.",
    "La météo est très chaude aujourd'hui.",
    "Ma parcelle manque d'eau.",
    "Il n'a pas plu depuis plusieurs jours.",
    "La récolte de ma parcelle est bonne.",
    "Les feuilles de mes plantes sont sèches.",
    "Le vent est très fort aujourd'hui.",
    "Je viens d'ajouter une nouvelle parcelle.",
    "Ma récolte est mauvaise cette année.",
    "La parcelle a suffisamment d'eau.",
    "Les plantes poussent très bien."
]

candidate_labels = [
    "positif",
    "negatif",
    "neutre",
    "agriculture",
    "meteo"
]

expected_labels = [
    "positif",
    "negatif",
    "positif",
    "negatif",
    "positif",
    "negatif",
    "positif",
    "negatif",
    "neutre",
    "positif",
    "meteo",
    "agriculture",
    "agriculture",
    "agriculture",
    "agriculture",
    "meteo",
    "agriculture",
    "agriculture",
    "agriculture",
    "agriculture"
]

predicted_labels = []

for text in texts:
    result = classifier(
        text,
        candidate_labels=candidate_labels
    )
    predicted_labels.append(result["labels"][0])

for i, (text, expected, predicted) in enumerate(
    zip(texts, expected_labels, predicted_labels), 1
):
    print(f"{i}. {text}")
    print(f"Attendu : {expected}")
    print(f"Prédit  : {predicted}")
    print()

accuracy = accuracy_score(expected_labels, predicted_labels)

print(f"Précision : {accuracy * 100:.2f}%")

errors = []

for i, (text, expected, predicted) in enumerate(
    zip(texts, expected_labels, predicted_labels), 1
):
    if expected != predicted:
        errors.append((i, text, expected, predicted))

print("\nErreurs :")

for error in errors[:3]:
    i, text, expected, predicted = error
    print(f"\nCas {i}")
    print(f"Texte   : {text}")
    print(f"Attendu : {expected}")
    print(f"Prédit  : {predicted}")