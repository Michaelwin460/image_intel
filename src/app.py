from flask import Flask, render_template, request
import os

from extractor import extract_all
from map_view import create_map
from timeline import create_timeline
from analyzer import analyze
from report import create_report

app = Flask(__name__)


@app.route("/")
def index():
    """
    דף הבית - טופס לבחירת תיקיית תמונות
    """
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze_images():
    """
    מקבל נתיב תיקייה, מריץ את כל המודולים, ומחזיר דו"ח HTML
    """
    folder_path = request.form.get("folder_path", "").strip()

    if not folder_path:
        return """
        <h2>שגיאה</h2>
        <p>לא הוזן נתיב לתיקייה.</p>
        <a href="/">חזרה לדף הבית</a>
        """, 400

    if not os.path.isdir(folder_path):
        return f"""
        <h2>שגיאה</h2>
        <p>התיקייה לא נמצאה:</p>
        <code>{folder_path}</code>
        <br><br>
        <a href="/">חזרה לדף הבית</a>
        """, 400

    try:
        # שלב 1: שליפת נתונים
        images_data = extract_all(folder_path)

        if not images_data:
            return f"""
            <h2>לא נמצאו תמונות</h2>
            <p>לא נמצאו קבצי תמונה נתמכים בתיקייה:</p>
            <code>{folder_path}</code>
            <br><br>
            <a href="/">חזרה לדף הבית</a>
            """, 200

        # שלב 2: יצירת מפה
        map_html = create_map(images_data)

        # שלב 3: יצירת ציר זמן
        timeline_html = create_timeline(images_data)

        # שלב 4: ניתוח
        analysis = analyze(images_data)

        # שלב 5: בניית דו"ח
        report_html = create_report(images_data, map_html, timeline_html, analysis)

        return report_html

    except Exception as e:
        return f"""
        <h2>אירעה שגיאה בזמן עיבוד הנתונים</h2>
        <p>{str(e)}</p>
        <br>
        <a href="/">חזרה לדף הבית</a>
        """, 500


if __name__ == "__main__":
    app.run(debug=True)