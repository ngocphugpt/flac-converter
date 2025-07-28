from flask import Flask, render_template, request, send_from_directory, jsonify
import os
import ffmpeg
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'converted'
ALLOWED_EXTENSIONS = {'mp3', 'mp4'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert_to_flac():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Empty filename'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(input_path)

        output_filename = os.path.splitext(filename)[0] + '.flac'
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)

        try:
            (
                ffmpeg
                .input(input_path)
                .output(output_path, format='flac')
                .overwrite_output()
                .run()
            )
        except ffmpeg.Error as e:
            return jsonify({'error': 'Conversion failed', 'details': str(e)}), 500

        return jsonify({'download_url': f'/download/{output_filename}'})

    return jsonify({'error': 'Unsupported file format'}), 400

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename, as_attachment=True)

if __name__ == "__main__":
    import os    port = int(os.environ.get("PORT", 5000))
        app.run(host="0.0.0.0", port=port)
        
