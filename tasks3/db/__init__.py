"""Database for tasks3"""

from .model import Base, Task
from .db import init, drop, purge
