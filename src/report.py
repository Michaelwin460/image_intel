from datetime import datetime


def create_report(images_data, map_html, timeline_html, analysis):
    """
    מרכיב את כל החלקים לדו"ח HTML אחד.
    """
    now = datetime.now().strftime("%d/%m/%Y %H:%M")

    total_images = analysis.get("total_images", 0)
    images_with_gps = analysis.get("images_with_gps", 0)
    unique_cameras = analysis.get("unique_cameras", [])
    insights = analysis.get("insights", [])
    date_range = analysis.get("date_range", {"start": None, "end": None})

    if insights:
        insights_html = "".join(f"<li>{insight}</li>" for insight in insights)
    else:
        insights_html = "<li>לא נמצאו תובנות מיוחדות.</li>"

    if unique_cameras:
        cameras_html = "".join(
            f"<span class='badge'>{camera}</span>"
            for camera in unique_cameras
        )
    else:
        cameras_html = "<p>לא נמצאו נתוני מכשירים.</p>"

    date_range_html = ""
    if date_range.get("start") and date_range.get("end"):
        date_range_html = f"""
        <div class="date-range">
            <strong>טווח תאריכים:</strong>
            {date_range["start"]} → {date_range["end"]}
        </div>
        """

    recent_images_html = ""
    sorted_with_datetime = [
        img for img in images_data if img.get("datetime")
    ]
    sorted_with_datetime = sorted(sorted_with_datetime, key=lambda x: x.get("datetime"))

    preview_images = sorted_with_datetime[:10]

    if preview_images:
        rows = ""
        for img in preview_images:
            camera_name = f'{img.get("camera_make") or "Unknown"} {img.get("camera_model") or "Unknown"}'.strip()
            gps_text = (
                f'{img.get("latitude")}, {img.get("longitude")}'
                if img.get("latitude") is not None and img.get("longitude") is not None
                else "No GPS"
            )

            rows += f"""
            <tr>
                <td>{img.get("filename", "")}</td>
                <td>{img.get("datetime", "") or "N/A"}</td>
                <td>{camera_name}</td>
                <td>{gps_text}</td>
            </tr>
            """

        recent_images_html = f"""
        <div class="section">
            <h2>תמונות לדוגמה</h2>
            <table>
                <thead>
                    <tr>
                        <th>קובץ</th>
                        <th>תאריך ושעה</th>
                        <th>מכשיר</th>
                        <th>מיקום</th>
                    </tr>
                </thead>
                <tbody>
                    {rows}
                </tbody>
            </table>
        </div>
        """

    html = f"""
    <!DOCTYPE html>
    <html lang="he" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>Image Intel Report</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
                background: #f4f6f8;
                color: #222;
            }}

            .header {{
                background: linear-gradient(135deg, #1B4F72, #2E86AB);
                color: white;
                padding: 30px;
                border-radius: 14px;
                text-align: center;
                box-shadow: 0 4px 12px rgba(0,0,0,0.12);
            }}

            .header h1 {{
                margin: 0 0 10px 0;
            }}

            .section {{
                background: white;
                padding: 22px;
                margin: 20px 0;
                border-radius: 12px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            }}

            .section h2 {{
                margin-top: 0;
                color: #1B4F72;
            }}

            .stats {{
                display: flex;
                gap: 16px;
                justify-content: center;
                flex-wrap: wrap;
                margin-top: 20px;
            }}

            .stat-card {{
                background: #EAF4FB;
                padding: 18px 26px;
                border-radius: 10px;
                min-width: 150px;
                text-align: center;
            }}

            .stat-number {{
                font-size: 2em;
                font-weight: bold;
                color: #1B4F72;
                margin-bottom: 6px;
            }}

            .badge {{
                background: #2E86AB;
                color: white;
                padding: 7px 12px;
                border-radius: 999px;
                margin: 4px;
                display: inline-block;
                font-size: 14px;
            }}

            ul {{
                padding-right: 20px;
            }}

            li {{
                margin-bottom: 10px;
            }}

            .date-range {{
                margin-top: 15px;
                padding: 12px;
                background: #f8fbfd;
                border-right: 4px solid #2E86AB;
                border-radius: 8px;
            }}

            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 12px;
                overflow: hidden;
                border-radius: 10px;
            }}

            th, td {{
                border-bottom: 1px solid #e6e6e6;
                padding: 12px;
                text-align: right;
                vertical-align: top;
            }}

            th {{
                background: #f3f7fa;
            }}

            .footer {{
                text-align: center;
                color: #777;
                margin-top: 30px;
                padding: 20px 0;
                font-size: 14px;
            }}

            .empty-note {{
                color: #666;
                background: #fafafa;
                padding: 12px;
                border-radius: 8px;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>Image Intel Report</h1>
            <p>דו"ח חילוץ מודיעין מתמונות</p>
            <p>נוצר ב-{now}</p>
        </div>

        <div class="section">
            <h2>סיכום</h2>
            <div class="stats">
                <div class="stat-card">
                    <div class="stat-number">{total_images}</div>
                    <div>תמונות</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{images_with_gps}</div>
                    <div>עם GPS</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{len(unique_cameras)}</div>
                    <div>מכשירים</div>
                </div>
            </div>
            {date_range_html}
        </div>

        <div class="section">
            <h2>תובנות מרכזיות</h2>
            <ul>
                {insights_html}
            </ul>
        </div>

        <div class="section">
            <h2>מפה אינטראקטיבית</h2>
            {map_html if map_html else "<div class='empty-note'>לא קיימת מפה להצגה.</div>"}
        </div>

        <div class="section">
            <h2>ציר זמן</h2>
            {timeline_html if timeline_html else "<div class='empty-note'>לא קיים ציר זמן להצגה.</div>"}
        </div>

        <div class="section">
            <h2>מכשירים</h2>
            {cameras_html}
        </div>

        {recent_images_html}

        <div class="footer">
            Image Intel | Final Project Report
        </div>
    </body>
    </html>
    """

    return html