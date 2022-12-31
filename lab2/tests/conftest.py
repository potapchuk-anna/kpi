import time

import pytest
from threading import Thread

from lab2.api import app


@pytest.fixture(scope="session", autouse=True)
def do_something(request):
    thread = Thread(target=app.run)
    thread.start()
    time.sleep(1)