from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent

load_dotenv()

from .apps import *
from .auth import *
from .aws import *
from .base import *
from .database import *
from .enviroment import *
from .files import *
from .i18n import *
from .middlewares import *
from .tests import *
