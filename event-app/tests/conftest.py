import os, sqlite3, pytest
import importlib
import pytest
import sys 

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

@pytest.fixture(scope="function")
def client(tmp_path):
    app_module = importlib.import_module("app")   
    app_module.DB_PATH = str(tmp_path / "test.db")
    app_module.init_db() 

    app_module.app.config.update({"TESTING": True})
    with app_module.app.test_client() as c:
        yield c