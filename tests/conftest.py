import os
import tempfile

import pytest

# Stub mode, throwaway audit log, known test secret: set before the app is imported.
os.environ.setdefault('LOG_DIR', tempfile.mkdtemp(prefix='m4-logs-'))
os.environ['JWT_SECRET'] = 'test-secret-' + 'x' * 40


@pytest.fixture(autouse=True)
def fresh_cache():
    from services.triage import model
    model.reset()
    yield
    model.reset()
