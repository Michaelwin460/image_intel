from map_view import create_map

def test_create_map():
    data = [
        {
            "filename": "test.jpg",
            "latitude": 32.0853,
            "longitude": 34.7818,
            "has_gps": True,
            "camera_make": "Test",
            "camera_model": "Camera",
            "datetime": "2025-01-01 10:00:00",
        }
    ]

    html = create_map(data)

    assert isinstance(html, str)
    assert "test.jpg" in html