from dataclasses import dataclass
from environs import Env


@dataclass
class DataBaseConfig:
    uri: str
    host: str
    password: str
    user: str
    database: str
    port: str


@dataclass
class TokenConfig:
    secret_key: str
    algorithm: str
    expire_minutes: int


@dataclass
class LinkConfig:
    host: str


@dataclass
class TestConfig:
    uri: str


@dataclass
class Config:
    db: DataBaseConfig
    token: TokenConfig
    link: LinkConfig
    test: TestConfig


def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    return Config(
        db=DataBaseConfig(
            uri=env.str('DB_URI'),
            host=env.str('DB_HOST'),
            password=env.str('DB_PASS'),
            user=env.str('DB_USER'),
            database=env.str('DB_NAME'),
            port=env.str('DB_PORT')
        ),
        token=TokenConfig(
            secret_key=env.str('SECRET_KEY'),
            algorithm=env.str('ALGORITHM'),
            expire_minutes=env.int('EXPIRE_MINUTES')
        ),
        link=LinkConfig(
            host=env.str('HOST')
        ),
        test=TestConfig(
            uri=env.str('TEST_URI')
        )
    )
