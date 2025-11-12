import os, pytest
from dataland_gui.webapp import create_app

@pytest.fixture()
def app():
    os.environ.setdefault("DATALAND_BASE_URL", "https://example.invalid")
    app = create_app()
    app.config.update({"TESTING": True})
    yield app

@pytest.fixture()
def client(app):
    return app.test_client()
