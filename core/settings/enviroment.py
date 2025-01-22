from enum import Enum
from os import getenv

SECRET_KEY = getenv("SECRET", "django-insecure")
DEBUG = getenv("DEBUG", "1") == "1"
ALLOWED_HOSTS = getenv("ALLOWED_HOSTS", "*,").split(",")

ENVENUM = Enum("Enviroment", "DEVELOPMENT PRODUCTION")
ENV = getenv("ENV", ENVENUM.DEVELOPMENT.name)

if ENV not in ENVENUM.__members__:
    raise ValueError("ENV not valid. Only values in Enviroment Enum are allowed")
