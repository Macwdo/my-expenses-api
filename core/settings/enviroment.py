from enum import Enum
from os import getenv

SECRET_KEY = getenv("SECRET", "django-insecure")
DEBUG = getenv("DEBUG", "1") == "1"
ALLOWED_HOSTS = getenv("ALLOWED_HOSTS", "*,").split(",")

ENVENUM = Enum("Enviroment", "DEVELOPMENT PRODUCTION")

# Environment Variables
ENV = getenv("ENV", ENVENUM.DEVELOPMENT.name)
OPENAI_ORGANIZATION = getenv("OPENAI_ORGANIZATION", "organization")
OPENAI_API_KEY = getenv("OPENAI_API_KEY", "api_key")

if ENV not in ENVENUM.__members__:
    raise ValueError("ENV not valid. Only values in Enviroment Enum are allowed")
