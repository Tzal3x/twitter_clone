from datetime import datetime, timedelta
import pytest
from app.helpers import Validator


def test_min_length():
    column_field = "abc"
    length = 4
    with pytest.raises(ValueError) as exc_info:
        Validator.min_length(column_field, length)
    assert str(exc_info.value) == \
        f"{column_field} is too short! Must be at least >= {length}."


def test_is_phone_number_valid():
    phone_number = "+306933395612"
    assert Validator.is_phone_number(phone_number) == phone_number


def test_is_phone_number_invalid():
    phone_number = "1234567890"
    with pytest.raises(ValueError):
        Validator.is_phone_number(phone_number)


def test_is_strong_valid():
    password = "Password123!"
    assert Validator.is_strong(password) == password


def test_is_strong_invalid_length():
    password = "pass"
    expected = "Password is not strong enough: "\
        "Needs at least 8 characters! Current: 4."
    with pytest.raises(ValueError) as exc_info:
        Validator.is_strong(password)
    assert str(exc_info.value) == expected


def test_is_strong_invalid_digit():
    password = "Password!"
    expected = "Password is not strong enough: Use at least 1 digit."
    with pytest.raises(ValueError) as exc_info:
        Validator.is_strong(password)
    assert str(exc_info.value) == expected


def test_is_strong_invalid_uppercase():
    password = "password1!"
    expected = "Password is not strong enough: "\
        "Use at least 1 uppercase letter."
    with pytest.raises(ValueError) as exc_info:
        Validator.is_strong(password)
    assert str(exc_info.value) == expected


def test_is_strong_invalid_lowercase():
    password = "PASSWORD1!"
    expected = "Password is not strong enough: "\
        "Use at least 1 lowercase letter."
    with pytest.raises(ValueError) as exc_info:
        Validator.is_strong(password)
    assert str(exc_info.value) == expected


def test_is_strong_invalid_symbol():
    password = "Password123"
    with pytest.raises(ValueError) as exc_info:
        Validator.is_strong(password)
    assert str(exc_info.value) == "Password is not strong enough: "\
        "Use at least 1 symbol."


def test_date_not_in_future_valid():
    date = datetime.utcnow().date()
    assert Validator.date_not_in_future(date) == date


def test_date_not_in_future_invalid():
    future_date = datetime.utcnow().date() + timedelta(days=1)
    with pytest.raises(ValueError) as exc_info:
        Validator.date_not_in_future(future_date)
    assert str(exc_info.value) == "Future date is not acceptable."
