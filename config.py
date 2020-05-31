import environs
from dataclasses import dataclass


"""Config saves the enviroment configuration of the signasl

Returns:
    Config -- Config DataClass
"""


@dataclass
class Config:
    postgres_uri: str = ""
    jwt_secret: bytes = ""


def load_config() -> Config:
    env = environs.Env()
    env.read_env()

    uri = env.str("POSTGRES_URI")
    secret = env.str("JWT_SECRET")

    return Config(uri, secret)
