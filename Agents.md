# Agents.md - Coding Style Guide for tasks3

This document outlines the coding style, design decisions, and conventions used in the tasks3 project. AI agents and human contributors should follow these guidelines when making changes to the codebase.

## Project Overview

**tasks3** is a command-line task management tool written in Python 3.12+ that allows users to create, edit, search, and track tasks associated with file system directories.

**Architecture:** Layered design with clear separation of concerns:
- **CLI Layer** (`cli.py`) - User interface using Click framework
- **Business Logic** (`tasks3.py`) - Core operations
- **Data Layer** (`db/`) - Database models and operations using SQLAlchemy
- **Configuration** (`config.py`) - Settings management

---

## Python Version and Dependencies

### Python Version
- **Minimum:** Python 3.12+
- Use modern Python features available in 3.12+

### Core Dependencies
- **Click** (8.1.6) - CLI framework
- **SQLAlchemy** (2.0.36) - ORM for database management
- **ruamel.yaml** (0.18.6) - YAML configuration handling

### Development Tools
- **pytest** - Testing framework
- **flake8** - Linting
- **black** (24.10.0) - Code formatting
- **tox** - Testing across Python versions
- **Sphinx** - Documentation generation

---

## Code Formatting

### Indentation and Line Length
- **Indent style:** 4 spaces (never tabs, except in Makefiles)
- **Max line length:** 88 characters (Black-compatible)
- **Line endings:** LF (Unix-style)
- **Charset:** UTF-8
- **Trailing whitespace:** Remove
- **Final newline:** Required

### Import Organization
Order imports in three groups, separated by blank lines:

```python
# 1. Standard library
import sys
from pathlib import Path
from typing import List, Optional, Callable

# 2. Third-party packages
import click
import sqlalchemy
from sqlalchemy import Column, Integer

# 3. Local imports
from tasks3.config import config
from tasks3.db import Task
```

---

## Naming Conventions

### Files and Directories
- **Python modules:** `snake_case` (e.g., `tasks3.py`, `config.py`, `models.py`)
- **Package directories:** lowercase (e.g., `tasks3/`, `db/`, `tests/`)
- **Test files:** `test_<module>.py` (e.g., `test_cli.py`, `test_db.py`)

### Functions and Methods
- **Style:** `snake_case`
- **Naming:** Use descriptive verbs (e.g., `add()`, `edit()`, `remove()`, `search()`)
- Examples: `session_scope()`, `load_config()`, `toggle_status()`

### Classes
- **Style:** `PascalCase`
- **Naming:** Clear, domain-specific names
- Examples: `Task`, `Config`, `Base`, `DBBackend`, `OutputFormat`

### Variables
- **Style:** `snake_case`
- **Naming:** Full words preferred over abbreviations (except common ones like `db`)
- Examples: `db_engine`, `db_path`, `output_format`

### Constants
- **Style:** `UPPER_SNAKE_CASE`
- Examples: `UUID_LENGTH`, `APP_DIR`, `DEFAULT_CONFIG_FILE_PATH`
- ANSI codes: `BOLD`, `UNDERLINE`, `STRIKETHROUGH`, `END`

---

## Type Annotations

### Requirements
- **All public functions** must have type annotations
- **Return types** must be explicitly declared
- Use `Optional[Type]` for nullable parameters
- Use `Generator` types for context managers

### Examples
```python
from typing import List, Optional, Callable, Generator

def search(
    db_engine: Engine,
    id: Optional[str] = None,
    title: Optional[str] = None,
    done: Optional[bool] = None,
) -> List[Task]:
    """Search tasks with optional filters."""
    ...

@contextmanager
def session_scope(bind: Engine) -> Generator[Session, Engine, None]:
    """Provide a transactional scope for database operations."""
    ...
```

---

## Documentation

### Module Docstrings
Every module must have a module-level docstring:

```python
"""Module-level docstring describing purpose."""
```

### Function Docstrings
Use Google/Sphinx hybrid style with `:param:` and `:returns:` tags:

```python
def function_name(param1: type, param2: type) -> return_type:
    """Brief description of what the function does.

    :param param1: Description of param1
    :param param2: Description of param2
    :returns: Description of return value
    """
```

### External Documentation
- **Format:** reStructuredText (.rst files)
- **Generator:** Sphinx with ReadTheDocs theme
- **Include:** README, CONTRIBUTING, HISTORY, installation, usage examples

---

## Design Patterns

### Single Dispatch Pattern
Use `@singledispatch` for function overloading:

```python
from functools import singledispatch

@singledispatch
def add(title: str, done: bool, ...) -> str:
    """Add with parameters."""
    ...

@add.register(Task)
def _(task: Task, db_engine: Engine) -> str:
    """Add with Task object."""
    ...
```

### Context Manager Pattern
Use context managers for resource management (especially database sessions):

```python
@contextmanager
def session_scope(bind: Engine) -> Generator[Session, Engine, None]:
    session = Session(bind=bind, expire_on_commit=False)
    try:
        yield session
        session.commit()
    except InvalidRequestError as e:
        session.rollback()
        raise e
    finally:
        session.close()
```

### Factory Pattern
Return appropriate function/object based on type:

```python
def __fmt(format: OutputFormat) -> Callable[[Task], str]:
    """Return formatter function based on format type."""
    if format == OutputFormat.oneline:
        return Task.one_line
    elif format == OutputFormat.short:
        return Task.short
    ...
```

### Dataclass Pattern
Use `@dataclass` for configuration and data structures:

```python
from dataclasses import dataclass, asdict

@dataclass
class Config:
    db: str = str(DEFAULT_DATA_FOLDER_PATH / "tasks.db")
    backend: str = DBBackend.sqlite.value
```

### Enum Pattern
Use `Enum` for fixed sets of values:

```python
from enum import Enum

class OutputFormat(Enum):
    oneline = "oneline"
    short = "short"
    yaml = "yaml"
    json = "json"
```

---

## Error Handling

### Database Operations
- Always use `session_scope()` context manager
- Explicit try/except/finally blocks
- Proper rollback on errors
- Clean up resources in finally blocks

### CLI Error Handling
- User-friendly error messages via Click
- Confirmation prompts for destructive operations
- Exit codes: 0 for success, 1 for errors

### Validation
- SQLAlchemy `CheckConstraint` for data validation
- Click's parameter types (`IntRange`, `Choice`, `Path`) for CLI validation
- Multi-layer validation (CLI, business logic, database)

---

## Testing

### Framework and Structure
- **Framework:** pytest
- **Test files:** Mirror source structure (`test_cli.py`, `test_db.py`, `test_tasks3.py`)
- **Naming:** `test_<feature>_<scenario>` (e.g., `test_db_init()`, `test_task_add1()`)

### Fixtures
Use pytest fixtures for test data and parametrization:

```python
@pytest.fixture(params=["sqlite"])
def db_backend(request) -> str:
    return request.param

@pytest.fixture(params=[0, 4], ids=["Not Urgent", "Very Urgent"])
def urgency(request) -> int:
    return request.param
```

### Test Isolation
- Use `tmp_path` fixture for database isolation
- Each test should be independent
- No shared state between tests

### Coverage Goals
- Unit tests for models, database operations, and business logic
- CLI integration tests using Click's `CliRunner`
- Aim for comprehensive coverage of core functionality

---

## CLI Design

### Click Framework Usage
- Use `@click.group()` for subcommands
- Distinguish between options (`--option`) and arguments
- Type validation: `IntRange`, `Choice`, `Path`
- Flag options: `is_flag=True`
- Multiple values: `multiple=True`
- Confirmation prompts: `click.confirm()`, `click.confirmation_option()`

### User Experience
- Extensive help text for all commands
- Show default values in help
- Provide both short (`-u`) and long (`--urgency`) option forms
- Require confirmation for destructive operations
- Clear, user-friendly error messages

### Output Formatting
- Support multiple output formats: oneline, short, yaml, json
- Use ANSI escape codes for terminal formatting
- Consistent use of emoji indicators (⏰ for urgency, 🚨 for importance)

---

## Database Design

### ORM Usage
- **ORM:** SQLAlchemy 2.0+ (modern version)
- **Declarative base** with automatic table naming
- **Session management:** Context manager pattern (`session_scope()`)

### Model Features
- UUID-based IDs (6 characters)
- Check constraints for data integrity
- JSON column for flexible data (e.g., tags)
- Unicode support for internationalization

### Query Patterns
```python
query: Query = Query(Task, session)
query = query.filter(Task.urgency == urgency)
results = query.order_by(Task.urgency, Task.importance).all()
```

### Session Configuration
- `expire_on_commit=False` for detached object access
- Explicit commit/rollback handling
- Proper cleanup in finally blocks

---

## Configuration Management

### Configuration Levels
1. **EditorConfig** (.editorconfig) - Editor settings
2. **Flake8** (setup.cfg, tox.ini) - Linting rules
3. **Application Config** (config.py) - User configuration

### Application Configuration
- **Format:** YAML-based
- **Auto-creation:** Create with defaults if missing
- **Location:** Application directory
- **Validation:** Type-safe with Enums and properties

### Property Pattern for Derived Values
```python
@property
def db_uri(self) -> str:
    return f"{self.db_backend.value}:///{self.db_path.absolute()}"
```

---

## File Organization

### Package Structure
```
tasks3/
├── tasks3/              # Main package
│   ├── __init__.py     # Package exports with __all__
│   ├── cli.py          # CLI interface
│   ├── tasks3.py       # Core business logic
│   ├── config.py       # Configuration management
│   └── db/             # Database layer
│       ├── __init__.py
│       ├── models.py   # SQLAlchemy models
│       ├── db.py       # DB operations
│       └── extension.py # DB utilities
├── tests/              # Test suite
├── docs/               # Sphinx documentation
└── [config files]
```

### Re-export Pattern
In `__init__.py`:

```python
from tasks3.tasks3 import add, edit, remove  # noqa: F401
__all__ = ["add", "edit", "remove", ...]
```

Use `# noqa: F401` only for intentional re-exports.

---

## Path Handling

### Best Practices
- Use `pathlib.Path` over string operations
- Normalize paths with `expanduser()` and `resolve()`
- Type annotate as `Path` not `str`

### Example
```python
from pathlib import Path

def load_config(config_file: Path = DEFAULT_CONFIG_FILE_PATH) -> Config:
    config_file = config_file.expanduser().resolve()
    ...
```

---

## String Formatting

### Preferred Approaches
1. **f-strings** (preferred for simple cases):
   ```python
   f"[{self.id}] {self.title}"
   ```

2. **Format method** (for complex cases):
   ```python
   "{}: {}".format(key, value)
   ```

---

## Code Quality Standards

### Linting
- **Tool:** flake8
- **Max line length:** 88 characters
- **Exclusions:** docs directory
- Run in CI pipeline

### Formatting
- **Tool:** black (24.10.0)
- **Line length:** 88 characters
- Run before committing

### Static Analysis
- No unused imports (except intentional re-exports with `# noqa`)
- Type hints throughout
- Docstrings for all public APIs

---

## Version Control and Releases

### Version Management
- **Tool:** bump2version
- **Versioning:** Semantic versioning (MAJOR.MINOR.PATCH)
- Version string kept in sync across multiple files

### Commit Messages
- Clear, descriptive commit messages
- Reference issue numbers when applicable

### Distribution
- PyPI package
- Universal wheel distribution
- Automated deployment via GitHub Actions

---

## Special Conventions

### Ellipsis Usage
Use `...` for intentional placeholders in functions that continue after complex logic:

```python
def toggle_status(...) -> Task:
    ...
    return task
    ...  # Intentional placeholder
```

### Default Parameter Handling
Dynamic defaults are acceptable:

```python
def search(folder: Path = Path.cwd()) -> List[Task]:
    ...
```

### Comments
- Minimal inline comments
- Code should be self-documenting
- Use docstrings for public APIs
- Comments only where logic is non-obvious

---

## Testing in CI/CD

### GitHub Actions
- Run tests on Python 3.12 and 3.13
- Matrix testing with tox
- Flake8 linting
- Automated on pull requests and pushes

### Test Commands
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=tasks3

# Run linting
flake8 tasks3

# Run tox for multiple Python versions
tox
```

---

## Key Principles

1. **Separation of Concerns:** Keep CLI, logic, and data layers separate
2. **Type Safety:** Use type annotations throughout
3. **Error Handling:** Always use proper exception handling and cleanup
4. **Testing:** Write tests for all new functionality
5. **Documentation:** Document all public APIs with docstrings
6. **User Experience:** Provide clear help text and error messages
7. **Code Style:** Follow Black formatting (88 chars, 4 spaces)
8. **Python Version:** Target Python 3.12+ only
9. **Simplicity:** Prefer simple, readable code over clever solutions
10. **Consistency:** Follow existing patterns in the codebase

---

## Summary for AI Agents

When contributing to this project:

1. ✅ **DO:**
   - Use type annotations for all functions
   - Write docstrings for public APIs
   - Use Black formatting (88 char lines, 4 spaces)
   - Follow the layered architecture
   - Write pytest tests for new features
   - Use context managers for resources
   - Use Enums for fixed value sets
   - Use pathlib.Path for file operations
   - Use Click for CLI commands
   - Use SQLAlchemy for database operations

2. ❌ **DON'T:**
   - Use tabs for indentation
   - Exceed 88 characters per line
   - Skip type annotations
   - Skip docstrings for public APIs
   - Mix layers (e.g., database code in CLI)
   - Use string paths instead of Path objects
   - Use bare except clauses
   - Leave trailing whitespace
   - Commit without running tests
   - Add dependencies without updating requirements.txt

3. 🔍 **BEFORE MAKING CHANGES:**
   - Read the existing code in the affected area
   - Follow the same patterns and style
   - Run tests to ensure nothing breaks
   - Check that flake8 passes
   - Update documentation if needed

---

*This guide reflects the current state of the tasks3 codebase and should be updated as the project evolves.*
