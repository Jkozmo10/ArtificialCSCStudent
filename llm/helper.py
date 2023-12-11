""" Helpful constants and types for the alpaca package """

import platform
from enum import Enum

OS_DICT = {
    "Windows": None,
    "Linux": "chat_linux",
    "Darwin": "chat_mac"
}

CHAT_FILE = OS_DICT.get(platform.system(), None)


class BulletType(Enum):
    """ Enum for the type of bullet point """
    EXPERIENCE = 1
    PROJECT = 2
