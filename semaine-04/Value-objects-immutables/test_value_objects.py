import pytest
from dataclasses import FrozenInstanceError

from value_objects import Money, GpsPoint, PhoneNumber


def test_money_addition():
    m1 = Money(100, "EUR")
    m2 = Money(50, "EUR")

    assert m1 + m2 == Money(150, "EUR")


def test_money_addition_devise_differente():
    m1 = Money(100, "EUR")
    m2 = Money(50, "USD")

    with pytest.raises(ValueError):
        m1 + m2


def test_distance():
    paris = GpsPoint(48.8566, 2.3522)
    londres = GpsPoint(51.5074, -0.1278)

    distance = paris.distance_to(londres)

    assert round(distance) == 344


def test_money_immutable():
    m = Money(100, "EUR")

    with pytest.raises(FrozenInstanceError):
        m.montant = 200


def test_gps_immutable():
    p = GpsPoint(48.85, 2.35)

    with pytest.raises(FrozenInstanceError):
        p.lat = 50


def test_phone_immutable():
    phone = PhoneNumber("0612345678", "FR")

    with pytest.raises(FrozenInstanceError):
        phone.numero = "0700000000"