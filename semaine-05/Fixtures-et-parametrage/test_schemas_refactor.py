import pytest
from pydantic import ValidationError
from sini.schemas import UserCreate, ParcelleCreate, RegionMali, CultureType


CAS_VALIDES_PHONE = [
    ("+223 70 00 00 00", "+22370000000"),
    ("+223 66 12 34 56", "+22366123456"),
    ("+223 90 00 00 00", "+22390000000"),
    ("+223 50 11 22 33", "+22350112233"),
    ("+223 82 99 88 77", "+22382998877"),
    ("+22320221100", "+22320221100"),
    (" +223 76 54 32 10 ", "+22376543210"),
    ("+223-71-23-45-67", "+22371234567"),
    ("+223.65.43.21.09", "+22365432109"),
    ("+223(70)000000", "+2237000000"),
]

IDS_VALIDES_PHONE = [
    "mali-valide-orange-7x-espaces",
    "mali-valide-malitel-6x-espaces",
    "mali-valide-telecel-9x-espaces",
    "mali-valide-prefixe-5x",
    "mali-valide-prefixe-8x",
    "mali-valide-fixe-2x-sans-espace",
    "mali-valide-espaces-extremites",
    "mali-valide-avec-tirets",
    "mali-valide-avec-points",
    "mali-valide-orange-compact",
]


CAS_INVALIDES_PHONE = [
    "+22312345678",
    "+33612345678",
    "+221770000000",
    "+2237000000",
    "+223700000000",
    "0700000000",
    "",
    "pas_un_numero",
    "+223 70 00 00 0",
    "++22370000000",
]

IDS_INVALIDES_PHONE = [
    "invalide-prefixe-mali-interdit-1x",
    "invalide-indicatif-france-33",
    "invalide-indicatif-senegal-221",
    "invalide-mali-7-chiffres-trop-court",
    "invalide-mali-9-chiffres-trop-long",
    "invalide-sans-indicatif-local",
    "invalide-chaine-vide",
    "invalide-texte-lettres",
    "invalide-mali-incomplet-espaces",
    "invalide-double-plus",
]


@pytest.mark.parametrize(
    "raw_phone, expected_phone",
    CAS_VALIDES_PHONE,
    ids=IDS_VALIDES_PHONE,
)
def test_user_create_phone_validation_success(raw_phone: str, expected_phone: str) -> None:
    user = UserCreate(
        full_name="Moussa Diarra",
        phone_number=raw_phone,
        region=RegionMali.BAMAKO,
        password="password123",
    )
    assert user.phone_number == expected_phone


@pytest.mark.parametrize(
    "invalid_phone",
    CAS_INVALIDES_PHONE,
    ids=IDS_INVALIDES_PHONE,
)
def test_user_create_phone_validation_failure(invalid_phone: str) -> None:
    with pytest.raises(ValidationError):
        UserCreate(
            full_name="Test User",
            phone_number=invalid_phone,
            region=RegionMali.BAMAKO,
            password="password123",
        )


def test_parcelle_superficie_must_be_positive() -> None:
    with pytest.raises(ValidationError):
        ParcelleCreate(
            name="Champ Invalide",
            superficie_ha=0.0,
            culture=CultureType.MAIS,
            region=RegionMali.SEGOU,
            owner_id=1,
        )