"""Database management functions"""

import tasks3.db as db
from sqlalchemy import create_engine
from sqlalchemy.orm import Query

from tasks3.db.extension import session_scope


def init(db_path: str):
    """Initialize a database to store Tasks at db_path

    :param db_path: uri to the database
    """
    engine = create_engine(db_path)
    db.Base.metadata.create_all(bind=engine)


def purge(db_path: str):
    """Remove all tasks from the database at db_path

    :param db_path: uri to the database
    """
    engine = create_engine(db_path)
    with session_scope(bind=engine) as session:
        Query(db.Task, session).delete()


def drop(db_path: str):
    """Drop the database at db_path

    :param db_path: uri to the database
    """
    engine = create_engine(db_path)
    db.Base.metadata.drop_all(bind=engine)
