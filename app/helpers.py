from dotenv import dotenv_values
from pathlib import Path



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
        "ACCESS_TOKEN_EXPIRE_MINUTES": int(env_vars["ACCESS_TOKEN_EXPIRE_MINUTES"]),
        "PASSWORD_HASH_SALT": env_vars["PASSWORD_HASH_SALT"],
    }
