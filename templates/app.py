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

    # Fast Image Loading
    img = Image.open(file.stream)
    
    # Resize extremely large images if width > 2000px to prevent server delay
    max_width = 2000
    if img.width > max_width:
        ratio = max_width / float(img.width)
        new_height = int(float(img.height) * float(ratio))
        img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)

    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
        
    output = io.BytesIO()
    # Fast Quality Compression (Quality 65 for ultra-fast response)
    img.save(output, format='JPEG', quality=65, optimize=True)
    output.seek(0)
    
    return send_file(output, mimetype='image/jpeg', as_attachment=True, download_name='compressed.jpg')

# Vercel handler
app = app
