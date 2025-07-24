from flask import Flask, render_template_string, request
from PIL import Image, ImageDraw, ImageFont
import pytesseract
import io
import base64

app = Flask(__name__)

HTML_TEMPLATE = '''
<!doctype html>
<title>Bulk Size Chart Translator</title>
<h1>Upload Size Chart Images (Chinese)</h1>
<form method=post enctype=multipart/form-data>
  <input type=file name=files multiple>
  <input type=submit value=Upload>
</form>
{% if results %}
  {% for result in results %}
    <h3>Original Image:</h3>
    <img src="data:image/jpeg;base64,{{ result['original_base64'] }}" width="400">
    <h3>Extracted Chinese Text:</h3>
    <pre>{{ result['extracted_text'] }}</pre>
    <h3>Translated Text (Placeholder):</h3>
    <pre>{{ result['translated_text'] }}</pre>
    <h3>Translated Image:</h3>
    <img src="data:image/jpeg;base64,{{ result['translated_base64'] }}" width="400">
    <hr>
  {% endfor %}
{% endif %}
'''

def image_to_base64(img):
    buf = io.BytesIO()
    img.save(buf, format='JPEG')
    base64_str = base64.b64encode(buf.getvalue()).decode()
    return base64_str

@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    if request.method == 'POST':
        files = request.files.getlist('files')
        for file in files:
            image = Image.open(file).convert('RGB')
            extracted_text = pytesseract.image_to_string(image, lang='chi_sim')

            translated_text = "[Translation unavailable here. Translate manually.]"

            new_img = Image.new('RGB', (image.width, image.height), color=(255, 255, 255))
            draw = ImageDraw.Draw(new_img)
            font = ImageFont.load_default()
            draw.multiline_text((10, 10), translated_text, font=font, fill=(0, 0, 0))

            results.append({
                'original_base64': image_to_base64(image),
                'translated_base64': image_to_base64(new_img),
                'extracted_text': extracted_text,
                'translated_text': translated_text
            })
    return render_template_string(HTML_TEMPLATE, results=results)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=7860)
