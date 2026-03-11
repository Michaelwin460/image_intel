# from map_view import create_map
#
# def test_create_map():
#     data = [
#         {
#             "filename": "test.jpg",
#             "latitude": 32.0853,
#             "longitude": 34.7818,
#             "has_gps": True,
#             "camera_make": "Test",
#             "camera_model": "Camera",
#             "datetime": "2025-01-01 10:00:00",
#         }
#     ]
#
#     html = create_map(data)
#
#     assert isinstance(html, str)
#     assert "test.jpg" in html



import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from src.map_view import create_map  # ← זה נשאר, השאר נמחק


def get_fake_data():
    return [
        {"filename": "t1.jpg", "latitude": 32.0, "longitude": 34.7,
         "has_gps": True, "camera_model": "Samsung", "datetime": "2025-01-12"},
        {"filename": "t2.jpg", "latitude": 31.7, "longitude": 35.2,
         "has_gps": True, "camera_model": "iPhone", "datetime": "2025-01-13"},
        {"filename": "t3.jpg", "latitude": None, "longitude": None,
         "has_gps": False, "camera_model": None, "datetime": None},
    ]

def test_create_map_returns_html():
    result = create_map(get_fake_data())
    assert isinstance(result, str)
    assert len(result) > 0

def test_create_map_handles_no_gps():
    no_gps = [{"filename": "x.jpg", "has_gps": False, "latitude": None,
               "longitude": None, "camera_model": None, "datetime": None}]
    result = create_map(no_gps)
    assert isinstance(result, str)

def test_create_map_handles_empty_list():
    result = create_map([])
    assert isinstance(result, str)