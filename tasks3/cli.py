"""Console script for tasks3."""
import sys
import os
import click


@click.group()
@click.version_option()
def main(args=None):
    """tasks3 is a commandline tool to create and manage tasks and todo lists."""
    return 0


@main.group()
def task():
    """Manage a task."""
    pass


@task.command()
@click.option(
    "-f",
    "--format",
    type=click.Choice(["YAML"]),
    default="YAML",
    help="Output format.",
    show_default=True,
)
@click.argument("id", type=str)
def show(format: str, id: str):
    """Print the Task in the specified FORMAT.

    ID is the id of the Task to be printed.
    """
    pass


@task.command()
@click.option(
    "-y/-n",
    "--yes/--no",
    default=False,
    help="Overwrite task data without confirmation?",
)
@click.argument("id", type=str)
def edit(yes: bool, id: str):
    """Edit a Task

    ID is the id of the Task to be edited.
    """
    pass


@task.command()
@click.option(
    "-y/-n", "--yes/--no", default=False, help="Delete task without confirmation?"
)
@click.argument("id", type=str)
def remove(yes: bool, id: str):
    """Remove a Task

    ID is the id of the Task to be removed.
    """
    pass


@task.command()
@click.option(
    "-T", "--title", default="Give a Title to this Task.", help="Title of the Task."
)
@click.option(
    "-u",
    "--urgency",
    type=click.IntRange(min=0, max=4, clamp=True),
    default=2,
    is_flag=True,
    flag_value=4,
    help="Level of urgency of the Task. "
    "Higher the value (max of 4) greater the urgency. "
    "Defaults to 2 when absent and 4 when present.",
)
@click.option(
    "-i",
    "--importance",
    type=click.IntRange(min=0, max=4, clamp=True),
    default=2,
    is_flag=True,
    flag_value=4,
    help="Level of importance of the Task. "
    "Higher the value (max of 4) greater the importance. "
    "Defaults to 2 when absent and 4 when present.",
)
@click.option("-t", "--tags", multiple=True, default=[], help="Tags for the Task.")
@click.option(
    "-a",
    "--anchor_to_folder",
    type=click.Path(exists=True, readable=False, file_okay=False, resolve_path=True),
    help="Anchor the Task to a specified directory or file.",
)
@click.option(
    "-d", "--description", default="", help="A short description of the Task."
)
@click.option(
    "-y/-n", "--yes/--no", default=False, help="Create task without confirmation?"
)
def add(
    title: str,
    urgency: int,
    importance: int,
    tags: tuple,
    anchor_to_folder: str,
    description: str,
    yes: bool,
):
    """Add a new task.
    """
    pass


@main.group()
def db():
    """Manage tasks3's database"""
    pass


@db.command()
@click.argument(
    "db",
    type=click.Path(dir_okay=False, writable=True),
    default=os.path.join(click.get_app_dir(__name__), "tasks.db"),
)
def init(db: str):
    """Initialize and setup the database at db.

    If db is not provide a database at system's default app directory is used.
    """
    pass


@db.command()
@click.confirmation_option(prompt="Are you sure you want to purge all tasks?")
@click.argument(
    "db",
    type=click.Path(dir_okay=False, writable=True),
    default=os.path.join(click.get_app_dir(__name__), "tasks.db"),
)
def purge(db: str):
    pass


@db.command()
@click.confirmation_option(prompt="Are you sure you want to drop the database?")
@click.argument(
    "db",
    type=click.Path(dir_okay=False, writable=True),
    default=os.path.join(click.get_app_dir(__name__), "tasks.db"),
)
def drop(db: str):
    pass


@db.command()
@click.confirmation_option(prompt="Are you sure you want to move the database?")
@click.option(
    "--db",
    type=click.Path(dir_okay=False, writable=True),
    default=os.path.join(click.get_app_dir(__name__), "tasks.db"),
    show_default=True,
    help="Location of database",
)
@click.argument(
    "dest_db",
    type=click.Path(dir_okay=False, writable=True),
    default=os.path.join(click.get_app_dir(__name__), "tasks.db"),
)
def move(db: str, dest_db: str):
    """Move tasks database to DEST_DB

    DEST_DB will be overwriten if it already exists.
    """
    pass


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
