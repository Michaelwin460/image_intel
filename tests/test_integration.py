import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.extractor import extract_all
from src.map_view import create_map
from src.timeline import create_timeline
from src.analyzer import analyze
from src.report import create_report


def test_full_pipeline():
    """הבדיקה הכי חשובה - כל הצינור מקצה לקצה"""
    images_data = extract_all("images/sample_data")
    assert len(images_data) > 0

    map_html = create_map(images_data)
    assert isinstance(map_html, str)

    timeline_html = create_timeline(images_data)
    assert isinstance(timeline_html, str)

    analysis = analyze(images_data)
    assert isinstance(analysis, dict)

    report_html = create_report(images_data, map_html, timeline_html, analysis)
    assert "<html" in report_html.lower()