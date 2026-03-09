import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = ROOT_DIR / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from app import app


def test_index_route():
    client = app.test_client()
    response = client.get("/")

    assert response.status_code == 200
    assert b"Image Intel" in response.data


def test_analyze_route_missing_folder():
    client = app.test_client()
    response = client.post("/analyze", data={})

    assert response.status_code == 400