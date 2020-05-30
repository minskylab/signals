import environs
from dataclasses import dataclass


"""Config saves the enviroment configuration of the signasl

Returns:
    [type] -- [description]
"""
@dataclass
class Config:
    postgres_host: str = ""
    postgres_password: str = ""


def load_config() -> Config:
    env = environs.Env()
    env.read_env()

    host = env.str("POSTGRES_HOST")
    password = env.str("POSTGRES_PASSWORD")

    return Config(host, password)
