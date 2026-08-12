from utils import timer

@timer
def calculer_surface_totale(superficies: list[float]) -> float:
    return sum(superficies)

parcelles = [1.5, 2.0, 3.2]

breakpoint()

total = calculer_surface_totale(parcelles)
print(f"Surface totale : {total}")


assert total == 6.7, f"Attendu 6.7 mais obtenu {total}"