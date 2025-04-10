import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv('.env')


@dataclass
class PostgresConfig:
    PG_USER: str = os.getenv("POSTGRES_USER")
    PG_PASS: str = os.getenv("POSTGRES_PASSWORD")
    PG_HOST: str = os.getenv("POSTGRES_HOST")
    PG_PORT: int = os.getenv("POSTGRES_PORT")
    PG_DB: str = os.getenv("POSTGRES_DB")

    @property
    def db_url(self):
        return f"postgresql+asyncpg://{self.PG_USER}:{self.PG_PASS}@{self.PG_HOST}:{self.PG_PORT}/{self.PG_DB}"


@dataclass
class WebConfig:
    """Web configuration"""
    SECRET_KEY: str = os.getenv('SECRET_KEY')
    USERNAME: str = os.getenv('ADMIN_USERNAME')
    PASSWD: str = os.getenv('ADMIN_PASSWORD')
    DOMAIN: str = os.getenv('WEBHOOK_DOMAIN')

@dataclass
class RedisConfig:
    pass


@dataclass
class BotConfig:
    TOKEN: str = os.getenv("BOT_TOKEN")


@dataclass
class Configuration:
    db = PostgresConfig()
    redis = RedisConfig()
    bot = BotConfig()
    web = WebConfig()

conf = Configuration()
