import re
from os import environ
from dotenv import load_dotenv
import phonenumbers
from datetime import datetime


def create_db_url() -> str:
    load_dotenv()
    db_url = "%s://%s:%s@%s/%s" % (
        environ["DB_SERVICE"],
        environ["DB_USERNAME"],
        environ["DB_PASSWORD"],
        environ["DB_HOST"],
        environ["DB_NAME"],
    )
    return db_url


def get_security_configs() -> dict[str]:
    load_dotenv()
    return {
        "TOKEN_CREATION_SECRET_KEY": environ["TOKEN_CREATION_SECRET_KEY"],
        "HASH_ALGORITHM": environ["HASH_ALGORITHM"],
        "ACCESS_TOKEN_EXPIRE_MINUTES": int(
            environ["ACCESS_TOKEN_EXPIRE_MINUTES"]
        ),
    }


class Validator:
    """
    Helper class that validates field constraints.
    """
    @staticmethod
    def min_length(column_field: str, length: int) -> str:
        """
        Checks if a string field
        """
        if len(column_field) < length:
            error_msg = (
                f"{column_field} is too short! "
                f"Must be at least >= {length}."
            )
            raise ValueError(error_msg)
        return column_field

    @staticmethod
    def is_phone_number(phone_number) -> str:
        try:
            pn = phonenumbers.parse(phone_number, None)
        except phonenumbers.NumberParseException as e:
            raise ValueError(f"Not a valid phone number: {str(e)}")
        if not phonenumbers.is_valid_number(pn):
            raise ValueError("Not a valid phone number.")
        return phone_number

    @staticmethod
    def is_strong(password: str) -> str:
        """
        Verify the strength of 'password'
        """
        min_password_len = 8
        length_error = (
            len(password) < min_password_len,
            f"Needs at least {min_password_len} characters! "
            f"Current: {len(password)}."
            )
        digit_error = (re.search(r"\d", password) is None,
                       "Use at least 1 digit.")

        uppercase_error = (re.search(r"[A-Z]", password) is None,
                           "Use at least 1 uppercase letter.")

        lowercase_error = (re.search(r"[a-z]", password) is None,
                           "Use at least 1 lowercase letter.")

        regex = r"[ !#$%&'()*+,-./[\\\]^_`{|}~"+r'"]'
        symbol_error = (re.search(regex, password) is None,
                        "Use at least 1 symbol.")

        errors = (length_error, digit_error,
                  uppercase_error, lowercase_error,
                  symbol_error)
        for error in errors:
            if error[0]:
                raise ValueError(f"Password is not strong enough: {error[1]}")
        return password

    @staticmethod
    def date_not_in_future(date) -> str:
        """
        Verify the strength of 'password'
        """
        present = datetime.now()
        if date > present.date():
            raise ValueError("Future date is not acceptable.")
        return date
