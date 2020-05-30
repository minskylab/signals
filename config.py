import environs
from dataclasses import dataclass


"""Config saves the enviroment configuration of the signasl

Returns:
    Config -- Config DataClass
"""


@dataclass
class Config:
    postgres_host: str = ""
    postgres_password: str = ""
    jwt_secret: bytes = ""


def load_config() -> Config:
    env = environs.Env()
    env.read_env()

    host = env.str("POSTGRES_HOST")
    password = env.str("POSTGRES_PASSWORD")
    secret = env.str("JWT_SECRET")

    return Config(host, password, secret)
