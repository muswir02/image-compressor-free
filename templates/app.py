import io
from flask import Flask, render_template, request, send_file
from PIL import Image

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compress', methods=['POST'])
def compress():
    if 'file' not in request.files:
        return "No file uploaded", 400

    file = request.files['file']
    if file.filename == '':
        return "No file selected", 400

    img = Image.open(file.stream)

    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")

    output = io.BytesIO()
    img.save(output, format='JPEG', quality=60, optimize=True)
    output.seek(0)

    return send_file(output, mimetype='image/jpeg', as_attachment=True, download_name='compressed.jpg')

if __name__ == '__main__':
    app.run(debug=True)
