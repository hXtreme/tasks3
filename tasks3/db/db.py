"""Database management functions"""

from sqlalchemy.engine import Engine
from sqlalchemy.orm import Query

import tasks3.db as db
from tasks3.db.extension import session_scope


def init(db_engine: Engine):
    """Initialize a database used by db_engine to store Tasks

    :param db_engine: engine for the database
    """
    db.Base.metadata.create_all(bind=db_engine)


def purge(db_engine: str):
    """Remove all tasks from the database

    :param db_engine: engine for the database
    """
    with session_scope(bind=db_engine) as session:
        Query(db.Task, session).delete()


def drop(db_engine: str):
    """Drop the database used by db_engine

    :param db_engine: engine for the database
    """
    db.Base.metadata.drop_all(bind=db_engine)
