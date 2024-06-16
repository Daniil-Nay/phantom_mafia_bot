from dataclasses import dataclass
from os import getenv

from dotenv import load_dotenv


@dataclass
class DatabaseConfig:
    """
    Path to POSTGRESQL db
    """
    database_user: str
    database_password: str
    database_name: str
    database_host: str
    database_port: str

@dataclass
class TelegramBot:
    """
    Data about Telegram bot and creator
    """
    token: str
    creator_id: int

@dataclass
class Config:
    """
    Configurations
    """
    tg_bot: TelegramBot
    db: DatabaseConfig


def load_config(
)->Config:
    """
    Uploading configuration data
    :return:
    """
    load_dotenv()
    return Config(tg_bot=TelegramBot(token=getenv("BOT_API_KEY"),
                                     creator_id=int(getenv("CREATOR_ID")
                                                    ),
                                     ),
                  db=DatabaseConfig(database_user=getenv("POSTGRES_USER"),
                                    database_name=getenv("POSTGRES_DB"),
                                    database_host=getenv("POSTGRES_HOST"),
                                    database_port=getenv("POSTGRES_PORT"),
                                    database_password=getenv('DATABASE_PASSWORD'),
                                    ),
                  )



