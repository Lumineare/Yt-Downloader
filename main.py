from flask import Flask, render_template, request, jsonify
from yt_dlp import YoutubeDL
import os

app = Flask(__name__)

def get_video_formats(url):
    """Retrieve available formats for a given video URL."""
    ydl_opts = {
        'quiet': True,
        'noplaylist': True,
        'cookiefile': 'cookies.txt'  # Path ke file cookies
    }
    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = [
                {
                    'format_id': f['format_id'],
                    'resolution': f.get('resolution', 'audio only'),
                    'ext': f['ext'],
                    'filesize': f.get('filesize', 'Unknown')
                }
                for f in info['formats'] if 'filesize' in f
            ]
            return formats
    except Exception as e:
        raise Exception(f"Error fetching formats: {str(e)}")

def download_video(url, format_id, output_path="downloads"):
    """Download video with the specified format."""
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    options = {
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        'format': format_id,
        'cookiefile': 'cookies.txt'  # Path ke file cookies
    }
    try:
        with YoutubeDL(options) as ydl:
            ydl.download([url])
    except Exception as e:
        raise Exception(f"Error downloading video: {str(e)}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_formats', methods=['POST'])
def get_formats():
    url = request.form['url']
    try:
        formats = get_video_formats(url)
        return jsonify({'success': True, 'formats': formats})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    format_id = request.form['format_id']
    output_path = "downloads"

    try:
        download_video(url, format_id, output_path)
        return jsonify({'success': True, 'message': 'Download successful! File saved to downloads folder.'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == "__main__":
    app.run(debug=True)
