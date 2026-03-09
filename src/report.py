"""
report.py - הרכבת דו"ח HTML סופי
צוות 3, זוג B

מקבל את כל החלקים ומחזיר HTML string מלא ומעוצב.

ראו docs/api_contract.md לפורמט הקלט.
"""

from datetime import datetime


def _build_images_table(images_data):
    """בונה טבלת תמונות מפורטת."""
    if not images_data:
        return "<p>אין נתונים.</p>"

    rows = ""
    for img in images_data:
        gps_cell = (
            f'<span class="badge badge-gps">✓ {img["latitude"]:.4f}, {img["longitude"]:.4f}</span>'
            if img.get("has_gps")
            else '<span class="badge badge-no">✗ אין</span>'
        )
        camera = img.get("camera_model") or img.get("camera_make") or "—"
        dt = img.get("datetime") or "—"
        rows += f"""
        <tr>
            <td class="td-filename">{img.get("filename", "—")}</td>
            <td>{dt}</td>
            <td>{camera}</td>
            <td>{gps_cell}</td>
        </tr>"""

    return f"""
    <div class="table-wrapper">
        <table>
            <thead>
                <tr>
                    <th>שם קובץ</th>
                    <th>תאריך ושעה</th>
                    <th>מכשיר</th>
                    <th>GPS</th>
                </tr>
            </thead>
            <tbody>{rows}</tbody>
        </table>
    </div>"""


def _build_cameras_section(analysis):
    """בונה סקשן מכשירים עם ספירה."""
    cameras = analysis.get("unique_cameras", [])
    if not cameras:
        return "<p>לא זוהו מכשירים.</p>"

    items = ""
    for cam in cameras:
        items += f'<div class="camera-chip">📷 {cam}</div>'
    return f'<div class="camera-grid">{items}</div>'


def _build_insights_section(analysis):
    """בונה סקשן תובנות."""
    insights = analysis.get("insights", [])
    if not insights:
        return "<p>אין תובנות זמינות.</p>"

    items = "".join(f'<li class="insight-item">{insight}</li>' for insight in insights)
    return f'<ul class="insights-list">{items}</ul>'


def create_report(images_data, map_html, timeline_html, analysis):
    """
    מרכיב את כל חלקי הדו"ח ל-HTML מלא.

    Args:
        images_data: רשימת מילונים מ-extract_all
        map_html:     HTML string מ-create_map
        timeline_html: HTML string מ-create_timeline
        analysis:     מילון מ-analyze (total_images, images_with_gps,
                      unique_cameras, date_range, insights)

    Returns:
        HTML string מלא (תוכן דף שלם)
    """
    now = datetime.now().strftime("%d/%m/%Y %H:%M")

    total        = analysis.get("total_images", 0)
    gps_count    = analysis.get("images_with_gps", 0)
    dt_count     = analysis.get("images_with_datetime", 0)
    cameras      = analysis.get("unique_cameras", [])
    date_range   = analysis.get("date_range", {})

    date_range_str = ""
    if date_range.get("start") and date_range.get("end"):
        date_range_str = f'<p class="date-range">📅 {date_range["start"]} — {date_range["end"]}</p>'

    images_table   = _build_images_table(images_data)
    cameras_section = _build_cameras_section(analysis)
    insights_section = _build_insights_section(analysis)

    return f"""<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Image Intel — דו"ח מודיעין</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Heebo:wght@300;400;600;700;900&display=swap" rel="stylesheet">
    <style>
        *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

        :root {{
            --navy:   #0d1b2a;
            --blue:   #1b4f72;
            --accent: #2e86ab;
            --light:  #e8f4fd;
            --warn:   #e67e22;
            --ok:     #27ae60;
            --bg:     #f0f4f8;
            --white:  #ffffff;
            --text:   #1a1a2e;
            --muted:  #6b7a8d;
            --border: #d0dce9;
            --radius: 12px;
            --shadow: 0 2px 12px rgba(13,27,42,0.10);
        }}

        body {{
            font-family: 'Heebo', sans-serif;
            background: var(--bg);
            color: var(--text);
            line-height: 1.6;
        }}

        /* ── HEADER ── */
        .report-header {{
            background: linear-gradient(135deg, var(--navy) 0%, var(--blue) 100%);
            color: white;
            padding: 48px 40px 36px;
            position: relative;
            overflow: hidden;
        }}
        .report-header::before {{
            content: '';
            position: absolute;
            top: -60px; right: -60px;
            width: 260px; height: 260px;
            border-radius: 50%;
            background: rgba(46,134,171,0.18);
        }}
        .report-header h1 {{
            font-size: 2.4rem;
            font-weight: 900;
            letter-spacing: -0.5px;
            position: relative;
        }}
        .report-header h1 span {{ color: #64d2ff; }}
        .report-header .subtitle {{
            font-size: 1rem;
            font-weight: 300;
            opacity: 0.75;
            margin-top: 6px;
        }}
        .report-header .generated {{
            position: absolute;
            bottom: 18px; left: 40px;
            font-size: 0.78rem;
            opacity: 0.55;
        }}

        /* ── LAYOUT ── */
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 32px 24px;
        }}

        .section {{
            background: var(--white);
            border-radius: var(--radius);
            box-shadow: var(--shadow);
            padding: 28px 32px;
            margin-bottom: 28px;
        }}

        .section-title {{
            font-size: 1.1rem;
            font-weight: 700;
            color: var(--blue);
            text-transform: uppercase;
            letter-spacing: 0.06em;
            border-bottom: 2px solid var(--light);
            padding-bottom: 12px;
            margin-bottom: 20px;
        }}

        /* ── STATS GRID ── */
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
            gap: 16px;
        }}
        .stat-card {{
            background: var(--light);
            border-radius: 10px;
            padding: 20px 16px;
            text-align: center;
            border-top: 4px solid var(--accent);
        }}
        .stat-card .stat-number {{
            font-size: 2.4rem;
            font-weight: 900;
            color: var(--blue);
            line-height: 1;
        }}
        .stat-card .stat-label {{
            font-size: 0.82rem;
            color: var(--muted);
            margin-top: 6px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.04em;
        }}
        .date-range {{
            text-align: center;
            color: var(--muted);
            font-size: 0.9rem;
            margin-top: 18px;
        }}

        /* ── INSIGHTS ── */
        .insights-list {{
            list-style: none;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }}
        .insight-item {{
            background: var(--light);
            border-right: 4px solid var(--accent);
            padding: 12px 16px;
            border-radius: 0 8px 8px 0;
            font-size: 0.95rem;
        }}

        /* ── CAMERAS ── */
        .camera-grid {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }}
        .camera-chip {{
            background: var(--navy);
            color: white;
            padding: 8px 16px;
            border-radius: 24px;
            font-size: 0.88rem;
            font-weight: 600;
        }}

        /* ── TABLE ── */
        .table-wrapper {{
            overflow-x: auto;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 0.88rem;
        }}
        th {{
            background: var(--navy);
            color: white;
            padding: 12px 14px;
            text-align: right;
            font-weight: 600;
            letter-spacing: 0.03em;
        }}
        td {{
            padding: 10px 14px;
            border-bottom: 1px solid var(--border);
            color: var(--text);
            vertical-align: middle;
        }}
        tr:last-child td {{ border-bottom: none; }}
        tr:nth-child(even) td {{ background: #fafcfe; }}
        .td-filename {{ font-family: monospace; font-size: 0.82rem; color: var(--blue); }}

        /* ── BADGES ── */
        .badge {{
            display: inline-block;
            padding: 3px 10px;
            border-radius: 12px;
            font-size: 0.78rem;
            font-weight: 700;
        }}
        .badge-gps  {{ background: #d4efdf; color: #1d6a3a; }}
        .badge-no   {{ background: #fce8e8; color: #a93226; }}

        /* ── MAP & TIMELINE wrappers ── */
        .map-wrapper {{ border-radius: 8px; overflow: hidden; }}
        .map-wrapper iframe, .map-wrapper > div {{ border-radius: 8px; }}

        /* ── FOOTER ── */
        .report-footer {{
            text-align: center;
            color: var(--muted);
            font-size: 0.8rem;
            padding: 24px;
        }}
    </style>
</head>
<body>

<div class="report-header">
    <h1>Image <span>Intel</span></h1>
    <p class="subtitle">דו"ח מודיעין חזותי — ניתוח נתוני EXIF מתמונות</p>
    <span class="generated">נוצר ב־{now}</span>
</div>

<div class="container">

    <!-- סיכום -->
    <div class="section">
        <div class="section-title">סיכום</div>
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-number">{total}</div>
                <div class="stat-label">תמונות</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{gps_count}</div>
                <div class="stat-label">עם GPS</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{dt_count}</div>
                <div class="stat-label">עם תאריך</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{len(cameras)}</div>
                <div class="stat-label">מכשירים</div>
            </div>
        </div>
        {date_range_str}
    </div>

    <!-- תובנות -->
    <div class="section">
        <div class="section-title">תובנות מרכזיות</div>
        {insights_section}
    </div>

    <!-- מפה -->
    <div class="section">
        <div class="section-title">מפה אינטראקטיבית</div>
        <div class="map-wrapper">
            {map_html}
        </div>
    </div>

    <!-- ציר זמן -->
    <div class="section">
        <div class="section-title">ציר זמן</div>
        {timeline_html}
    </div>

    <!-- מכשירים -->
    <div class="section">
        <div class="section-title">מכשירים שזוהו</div>
        {cameras_section}
    </div>

    <!-- טבלה מלאה -->
    <div class="section">
        <div class="section-title">כל התמונות — פירוט מלא</div>
        {images_table}
    </div>

</div>

<div class="report-footer">Image Intel &nbsp;|&nbsp; האקתון 2025</div>

</body>
</html>"""


# ── בדיקה מהירה ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    fake_images = [
        {"filename": "IMG_001.jpg", "datetime": "2025:01:12 08:30:00",
         "camera_make": "Samsung", "camera_model": "Galaxy S23",
         "has_gps": True, "latitude": 32.0853, "longitude": 34.7818},
        {"filename": "IMG_002.jpg", "datetime": "2025:01:12 11:15:00",
         "camera_make": "Apple", "camera_model": "iPhone 15 Pro",
         "has_gps": False, "latitude": None, "longitude": None},
    ]
    fake_analysis = {
        "total_images": 2,
        "images_with_gps": 1,
        "images_with_datetime": 2,
        "unique_cameras": ["Samsung Galaxy S23", "Apple iPhone 15 Pro"],
        "date_range": {"start": "2025-01-12", "end": "2025-01-12"},
        "insights": [
            "נמצאו 2 מכשירים שונים",
            "תמונה אחת עם GPS",
        ]
    }

    html = create_report(
        fake_images,
        map_html="<p style='color:gray'>[מפה תוצג כאן]</p>",
        timeline_html="<p style='color:gray'>[ציר זמן יוצג כאן]</p>",
        analysis=fake_analysis
    )
    with open("test_report.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("✅  test_report.html נשמר")