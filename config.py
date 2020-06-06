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
    root_token: str = ""
    mode: str = "full"


def load_config() -> Config:
    env = environs.Env()
    env.read_env()

    uri = env.str("POSTGRES_URI")
    secret = env.str("JWT_SECRET", "")
    root_token = env.str("ROOT_TOKEN", "")
    mode = env.str("MODE", "full")

    return Config(uri, secret, root_token, mode)
