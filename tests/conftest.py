import os
import tempfile

import pytest

from ferret import create_app
from ferret import db
from ferret import init_db


@pytest.fixture
def app():
    """Create and configure a new ferret instance for each test."""
    # create a temporary file to isolate the database for each test
    db_fd, db_path = tempfile.mkstemp()
    # create the ferret with common test config
    app = create_app({"TESTING": True, "DATABASE": db_path})

    with app.app_context():
        init_db()

    yield app

    # close and remove the temporary database
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    """A test client for the ferret."""
    return app.test_client()

