from datetime import datetime
import extractor


def analyze(images_data):
    """
    מנתח את נתוני התמונות ומפיק תובנות מודיעיניות.
    """
    # חישוב נתונים בסיסיים
    total_images = len(images_data)
    images_with_gps = len([img for img in images_data if img.get("gps")])
    dated_images = [img for img in images_data if img.get("datetime")]

    # חילוץ מכשירים ייחודיים
    cameras = list(set([img.get("camera_model") for img in images_data if img.get("camera_model")]))

    # טווח תאריכים
    date_range = {"start": None, "end": None}
    if dated_images:
        sorted_dates = sorted([img["datetime"] for img in dated_images])
        date_range["start"] = sorted_dates[0]
        date_range["end"] = sorted_dates[-1]

    # זיהוי תובנות (Insights)
    insights = []

    # 1. תובנת החלפת מכשירים
    if len(cameras) > 1:
        insights.append(f"נמצאו {len(cameras)} מכשירים שונים - ייתכן שהסוכן החליף מכשירים.")

    # 2. בדיקת רצף החלפות
    dated_images.sort(key=lambda x: x["datetime"])
    for i in range(1, len(dated_images)):
        prev_cam = dated_images[i - 1].get("camera_model")
        curr_cam = dated_images[i].get("camera_model")
        if prev_cam and curr_cam and prev_cam != curr_cam:
            insights.append(f"בתאריך {dated_images[i]['datetime']} הסוכן עבר מ-{prev_cam} ל-{curr_cam}.")

    # 3. תובנת GPS
    if images_with_gps > 0:
        insights.append(f"קיימים נתוני מיקום עבור {images_with_gps} תמונות. ניתן לבצע איכון גיאוגרפי.")

    # בניית המילון הסופי לפי הפורמט הנדרש
    return {
        "total_images": total_images,
        "images_with_gps": images_with_gps,
        "images_with_datetime": len(dated_images),
        "unique_cameras": cameras,
        "date_range": date_range,
        "insights": insights
    }



# # --- אזור הרצה לבדיקה (Mock Data) ---
# if __name__ == "__main__":
#     test_data = [
#         {"filename": "a.jpg", "datetime": "2025-01-12 10:00", "camera_model": "Samsung S23", "gps": True},
#         {"filename": "b.jpg", "datetime": "2025-01-13 12:00", "camera_model": "iPhone 15 Pro", "gps": False},
#     ]
#
#     analysis_results = analyze(test_data)
#
#     import json
#
#     print(json.dumps(analysis_results, indent=4, ensure_ascii=False))