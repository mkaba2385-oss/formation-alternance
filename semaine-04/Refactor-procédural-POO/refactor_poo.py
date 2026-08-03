class Produit:
    def __init__(self, nom:str, prix:float):
        self.nom = nom
        self._prix = prix
    
    @property
    def prix(self):
        return self._prix

    @classmethod
    def depuis_dict(cls, data):
        return cls(data["nom"], data["prix"])

class Article:
    def __init__(self, produit: Produit, quantite: int):
        self.produit = produit
        self.quantite = quantite

    def sous_total(self):
        return self.produit.prix * self.quantite


class Panier:
    def __init__(self):
        self.articles = []

    def ajouter(self, article: Article):
        self.articles.append(article)

    def total(self):
        return sum(article.sous_total() for article in self.articles)

class PanierPromo(Panier):
    def __init__(self, reduction: float):
        super().__init__()
        self.reduction = reduction

    def total(self):
        return super().total() * (1 - self.reduction)


# Version équivalente au script procédural

donnees = [
    {"nom": "Pomme", "prix": 1.5, "quantite": 4},
    {"nom": "Lait", "prix": 2.0, "quantite": 2},
]

panier = Panier()

for d in donnees:
    produit = Produit.depuis_dict(d)
    article = Article(produit, d["quantite"])
    panier.ajouter(article)

print("Total :", panier.total())


# Tests
# Test 1 : équivalence avec le script procédural
assert panier.total() == 10.0

# Test 2 : property
p = Produit("Pain", 1.2)
assert p.prix == 1.2

# Test 3 : héritage
promo = PanierPromo(0.10)

promo.ajouter(Article(Produit("Pomme", 1.5), 4))
promo.ajouter(Article(Produit("Lait", 2.0), 2))

assert promo.total() == 9.0

print("Tous les tests sont réussis.")