"""Main module."""

import tasks3.db as db

from typing import Set
from sqlalchemy import create_engine
from sqlalchemy.orm import Query


def add(
    title: str,
    urgency: int,
    importance: int,
    tags: Set[str],
    anchor_folder: str,
    description: str,
    db_path: str,
):
    """Add a task

    :param title: Title for the new task.
    :param urgency: Urgency level[0-4] for the new task.
    :param importance: Importance level[0-4] for the new task.
    :param tags: Set of tags to apply to the new task.
    :param anchor_folder: Anchor this task to a particular directory or file.
    :param description: Description of the task.
    :param db_path: Path to the tasks database.
    """
    task = db.Task(
        title=title,
        urgency=urgency,
        importance=importance,
        tags=tags,
        folder=anchor_folder,
        description=description,
    )
    db_engine = create_engine(f"{db_path}")
    with db.session_scope(db_engine) as session:
        session.add(task)


def edit(
    id: str,
    db_path: str,
    title: str = None,
    urgency: int = None,
    importance: int = None,
    tags: Set[str] = None,
    anchor_folder: str = None,
    description: str = None,
):
    """Edit a task

    :param id: ID of the task to edit.
    :param db_path: Path to the tasks database.
    :param title: Update title of the task.
    :param urgency: Update urgency level[0-4] of the task.
    :param importance: Update importance level[0-4] of the task.
    :param tags: Set of tags to apply to the new task.
    :param anchor_folder: Anchor this task to a particular directory or file.
    :param description: Description of the task.
    """
    db_engine = create_engine(f"{db_path}")
    task: db.Task
    with db.session_scope(db_engine) as session:
        task = Query(db.Task, session).filter_by(id=id).one()
        if title:
            task.title = title
        if urgency:
            task.urgency = urgency
        if importance:
            task.importance = importance
        if tags:
            task.tags = tags
        if anchor_folder:
            task.folder = anchor_folder
        if description:
            task.description = description
        session.add(task)


def remove(id: str, db_path: str) -> db.Task:
    """Remove a Task

    :param id: ID of the task to remove.
    :param db_path: Path to the tasks database.
    """
    db_engine = create_engine(f"{db_path}")
    task: db.Task
    with db.session_scope(db_engine) as session:
        task = Query(db.Task, session).filter_by(id=id).one()
        session.delete(task)
    return task
