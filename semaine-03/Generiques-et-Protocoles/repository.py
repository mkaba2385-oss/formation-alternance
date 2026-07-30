from __future__ import annotations

import json
from collections.abc import Sequence
from typing import Protocol, Self, TypeVar, Generic, cast


class Serializable(Protocol):
    def to_dict(self) -> dict[str, object]:
        ...

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> Self:
        ...


T = TypeVar("T")


class Repository(Generic[T]):
    def __init__(self) -> None:
        self._items: list[T] = []

    def add(self, item: T) -> None:
        self._items.append(item)

    def get(self, index: int) -> T:
        return self._items[index]

    def list(self) -> list[T]:
        return self._items.copy()

    def delete(self, index: int) -> None:
        del self._items[index]


def save_to_json(items: Sequence[Serializable], path: str) -> None:
    data = [item.to_dict() for item in items]

    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


class Person:
    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age

    def to_dict(self) -> dict[str, object]:
        return {
            "name": self.name,
            "age": self.age,
        }

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> Self:
        name = cast(str, data["name"])
        age = cast(int, data["age"])
        return cls(name, age)


class Product:
    def __init__(self, name: str, price: float) -> None:
        self.name = name
        self.price = price

    def to_dict(self) -> dict[str, object]:
        return {
            "name": self.name,
            "price": self.price,
        }

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> Self:
        name = cast(str, data["name"])
        price = cast(float, data["price"])
        return cls(name, price)


class Animal:
    def __init__(self, species: str) -> None:
        self.species = species


def main() -> None:
    people = Repository[Person]()

    people.add(Person("Moussa", 22))
    people.add(Person("Kabine", 35))

    save_to_json(people.list(), "people.json")

    products = Repository[Product]()

    products.add(Product("iphone16", 999.99))
    products.add(Product("Samsung", 100.50))

    save_to_json(products.list(), "products.json")

    animals = Repository[Animal]()
    animals.add(Animal("chien"))

    # Décommente cette ligne pour voir l'erreur de mypy.
    # save_to_json(animals.list(), "animals.json")


if __name__ == "__main__":
    main()