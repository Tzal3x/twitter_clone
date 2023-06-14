import re
from dotenv import dotenv_values
from pathlib import Path
import phonenumbers


def load_configs() -> dict:
    """
    Load configuration variables about the database etc.
    """
    path_to_env = Path(__file__).parent.parent.joinpath('configs.env')
    return dotenv_values(path_to_env)


def create_db_url() -> str:
    env_vars = load_configs()
    db_url = "%s://%s:%s@%s/%s" % (
        env_vars["DB_SERVICE"],
        env_vars["DB_USERNAME"],
        env_vars["DB_PASSWORD"],
        env_vars["DB_HOST"],
        env_vars["DB_NAME"],
    )
    return db_url


def get_security_configs() -> dict[str]:
    env_vars = load_configs()
    return {
        "TOKEN_CREATION_SECRET_KEY": env_vars["TOKEN_CREATION_SECRET_KEY"],
        "HASH_ALGORITHM": env_vars["HASH_ALGORITHM"],
        "ACCESS_TOKEN_EXPIRE_MINUTES": int(
            env_vars["ACCESS_TOKEN_EXPIRE_MINUTES"]
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
        pn = phonenumbers.parse(phone_number, None)
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
