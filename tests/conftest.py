import copy
import pytest

from src import app as app_module


@pytest.fixture(autouse=True)
def reset_activities():
    """Restore the in-memory activity data after each test.

    The backend stores its state in a global dictionary; tests mutate
    it via HTTP requests.  To keep tests isolated we copy the original
    and restore it when a test finishes.
    """

    original = copy.deepcopy(app_module.activities)
    yield
    # restore contents of the existing dict so imported references stay valid
    app_module.activities.clear()
    app_module.activities.update(original)
