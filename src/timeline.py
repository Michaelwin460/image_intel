def create_timeline(images_data):
    dated_images = [img for img in images_data if img["datetime"]]
    dated_images.sort(key=lambda x: x["datetime"])

    html = '<div style="position:relative; padding:20px;">'
    html += '<div style="position:absolute; left:50%; width:2px; height:100%; background:#333;"></div>'

    for i, img in enumerate(dated_images):
        side = "left" if i % 2 == 0 else "right"
        html += f'''
        <div style="margin:20px 0; text-align:{side};">
            <strong>{img["datetime"]}</strong><br>
            {img["filename"]}<br>
            <small>{img.get("camera_model", "Unknown")}</small>
        </div>'''

    html += '</div>'
    return html