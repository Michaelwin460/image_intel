from src.report import create_report


def test_create_report_returns_full_html():
    images_data = [
        {
            "filename": "test1.jpg",
            "datetime": "2025-01-12 08:30:00",
            "latitude": 32.0853,
            "longitude": 34.7818,
            "camera_make": "Samsung",
            "camera_model": "Galaxy S23",
            "has_gps": True,
        }
    ]

    map_html = "<div>Map Placeholder</div>"
    timeline_html = "<div>Timeline Placeholder</div>"
    analysis = {
        "total_images": 1,
        "images_with_gps": 1,
        "unique_cameras": ["Samsung Galaxy S23"],
        "date_range": {"start": "2025-01-12", "end": "2025-01-12"},
        "insights": ["Test insight"]
    }

    html = create_report(images_data, map_html, timeline_html, analysis)

    assert isinstance(html, str)
    assert "<html" in html.lower()
    assert "Image Intel Report" in html
    assert "Map Placeholder" in html
    assert "Timeline Placeholder" in html
    assert "Test insight" in html