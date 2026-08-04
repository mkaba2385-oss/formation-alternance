import json


class Field:
    def __init__(self, field_type, default=None, max_length=None):
        self.field_type = field_type
        self.default = default
        self.max_length = max_length
        self.private_name = None

    def __set_name__(self, owner, name):
        self.private_name = "_" + name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.private_name, self.default)

    def __set__(self, instance, value):
        if not isinstance(value, self.field_type):
            raise TypeError(
                f"{self.private_name[1:]} doit être de type {self.field_type.__name__}"
            )

        if self.field_type == str and self.max_length is not None:
            if len(value) > self.max_length:
                raise ValueError(
                    f"{self.private_name[1:]} dépasse {self.max_length} caractères."
                )

        setattr(instance, self.private_name, value)


class Model:

    def __init_subclass__(cls):
        super().__init_subclass__()
        cls._fields = {}

        for name, value in cls.__dict__.items():
            if isinstance(value, Field):
                cls._fields[name] = value

    def __init__(self, **kwargs):
        for name, field in self._fields.items():
            value = kwargs.get(name, field.default)
            setattr(self, name, value)

    
    def save(self):
        data = {}

        for field in self._fields:
            data[field] = getattr(self, field)

        filename = f"{self.__class__.__name__}.json"

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

        print(f"{filename} sauvegardé.")

    
    @classmethod
    def load(cls):
        filename = f"{cls.__name__}.json"

        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)

        return cls(**data)


class User(Model):
    name = Field(str, max_length=100)
    age = Field(int, default=18)


# Exemple d'utilisation

u = User(name="Alice")

print("Nom :", u.name)
print("Âge :", u.age)

u.age = 25

u.save()

u2 = User.load()

print("\nObjet chargé :")
print("Nom :", u2.name)
print("Âge :", u2.age)