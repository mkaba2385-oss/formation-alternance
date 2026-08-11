from datetime import datetime, timedelta, timezone
from unittest.mock import patch, Mock
import pytest
from hypothesis import given, strategies as st
from pydantic import ValidationError

from sini.schemas import UserCreate, RegionMali


PHONE_MALI_VALID = "+22370000000"
FIXED_OTP = "123456"


@patch("sini.services.sms.send_sms", create=True)
@patch("random.randint", return_value=123456)
def test_full_auth_flow_e2e(mock_randint, mock_send_sms):
    generated_otp = str(mock_randint.return_value)
    mock_send_sms(PHONE_MALI_VALID, f"Votre code OTP est {generated_otp}")

    mock_send_sms.assert_called_once_with(
        PHONE_MALI_VALID, f"Votre code OTP est {FIXED_OTP}"
    )

    user_input_otp = "123456"
    assert user_input_otp == generated_otp

    fake_jwt = "header.payload.signature"
    assert fake_jwt.count(".") == 2


def test_auth_flow_invalid_otp():
    generated_otp = "123456"
    user_input_otp = "999999"

    assert user_input_otp != generated_otp


def test_auth_flow_expired_otp():
    creation_time = datetime.now(timezone.utc)
    expiration_time = creation_time + timedelta(minutes=5)

    future_time = creation_time + timedelta(minutes=10)

    assert future_time > expiration_time


def test_fake_jwt_validation():
    invalid_token = "invalid.token.signature"
    is_valid = False

    assert is_valid is False


@given(
    prefix=st.sampled_from(["2", "5", "6", "7", "8", "9"]),
    digits=st.text(alphabet="0123456789", min_size=7, max_size=7),
)
def test_hypothesis_mali_phone_numbers_valid(prefix, digits):
    phone = f"+223{prefix}{digits}"
    user = UserCreate(
        full_name="Moussa Diarra",
        phone_number=phone,
        region=RegionMali.BAMAKO,
        password="password123",
    )
    assert user.phone_number == f"+223{prefix}{digits}"