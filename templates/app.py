import io
from flask import Flask, render_template, request, send_file
from PIL import Image

app = Flask(__name__)

# Essential for Vercel Serverless Routing
app.debug = False

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/compress', methods=['POST'])
def compress():
    try:
        if 'file' not in request.files:
            return "No file uploaded", 400
        
        file = request.files['file']
        if file.filename == '':
            return "No file selected", 400

        img = Image.open(file.stream)
        
        # Auto-Resize if image is too large (prevents timeout on free server)
        max_size = (1920, 1920)
        img.thumbnail(max_size, Image.Resampling.LANCZOS)

        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
            
        output = io.BytesIO()
        img.save(output, format='JPEG', quality=60, optimize=True)
        output.seek(0)
        
        return send_file(
            output, 
            mimetype='image/jpeg', 
            as_attachment=True, 
            download_name='compressed.jpg'
        )
    except Exception as e:
        return str(e), 500

# Vercel needs this exact variable exported
app = app
