#!/usr/bin/env python

"""Tests for tasks3's Task ORM"""

import pytest

from tasks3.db import Task


@pytest.fixture(params=["Title", "Sample Title0"])
def title(request):
    return request.param


@pytest.fixture(params=[x for x in range(5)])
def urgency(request):
    return request.param


@pytest.fixture(params=[x for x in range(5)])
def importance(request):
    return request.param


def test_task_create(title, urgency, importance):
    task = Task(title=title, urgency=urgency, importance=importance, tags=["pytest"],)
    assert task.title == title
    assert task.urgency == urgency
    assert task.importance == importance
    assert "pytest" in task.tags
