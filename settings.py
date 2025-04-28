# settings.py

from pathlib import Path
from dotenv import load_dotenv
import configparser
import os


BASE_DIR     = Path(__file__).resolve().parent
ENV_PATH     = BASE_DIR / '.env'
CONFIG_PATH  = BASE_DIR / 'config.ini'

load_dotenv(dotenv_path=ENV_PATH)

config_parser = configparser.ConfigParser()
config_parser.read(CONFIG_PATH)


def str_to_bool(value: str) -> bool:
    return value.lower() in {'true', '1', 'yes'}


class General:
    APP_NAME       = config_parser.get('GENERAL', 'APP_NAME', fallback='Rewardify')
    SAVE_DIRECTORY = config_parser.get('GENERAL', 'SAVE_DIRECTORY', fallback='__cache__/users')
    ENVIRONMENT    = os.getenv('ENV', 'production')
    DEBUG          = str_to_bool(os.getenv('DEBUG', 'false'))

class AI:
    PROVIDER       = config_parser.get('AI', 'MODEL_PROVIDER', fallback='openai')
    DEFAULT_MODEL  = config_parser.get('AI', 'DEFAULT_MODEL', fallback='gpt-4')
    TEMPERATURE    = float(config_parser.get('AI', 'TEMPERATURE', fallback='0.7'))
    MAX_TOKENS     = int(config_parser.get('AI', 'MAX_TOKENS', fallback='512'))
    API_KEY        = os.getenv('OPENAI_API_KEY')
    MODEL          = os.getenv('OPENAI_MODEL', DEFAULT_MODEL)

class Database:
    HOST           = os.getenv('DB_HOST')
    PORT           = os.getenv('DB_PORT')
    USERNAME       = os.getenv('DB_USERNAME')
    PASSWORD       = os.getenv('DB_PASSWORD')
    DATABASE       = os.getenv('DB_DATABASE')
    SSLMODE        = os.getenv('DB_SSLMODE')

class Auth:
    SECRET_KEY     = os.getenv('JWT_SECRET_KEY')
    ALGORITHM      = os.getenv('JWT_ALGORITHM', 'HS256')
    EXPIRES_DAYS   = int(os.getenv('EXPIRES_DAYS', '7'))


general  = General()
ai       = AI()
database = Database()
auth     = Auth()

__all__ = ["general", "ai", "database", "auth"]