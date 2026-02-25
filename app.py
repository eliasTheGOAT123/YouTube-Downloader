"""
YouTube Video Downloader - Web Application
A Flask web application to download videos from YouTube
"""

import os
import sys
import threading
from flask import Flask, render_template, request, jsonify

# Install Flask if not available
def install_dependencies():
    try:
        import flask
    except ImportError:
        print("Installing Flask...")
        os.system("pip install flask")
    
    try:
        import yt_dlp
    except ImportError:
        print("Installing yt-dlp...")
        os.system("pip install yt-dlp")

install_dependencies()

from flask import Flask, render_template, request, jsonify
import yt_dlp

app = Flask(__name__)
app.template_folder = 'templates'

# Default download folder
DEFAULT_DOWNLOAD_DIR = os.path.join(os.path.expanduser('~'), 'Downloads', 'YouTube')


def get_output_path(user_choice):
    """Get the output path based on user selection."""
    home = os.path.expanduser('~')
    
    paths = {
        'downloads': os.path.join(home, 'Downloads'),
        'videos': os.path.join(home, 'Videos'),
        'desktop': os.path.join(home, 'Desktop'),
    }
    
    if user_choice and user_choice in paths:
        download_dir = paths[user_choice]
    else:
        download_dir = DEFAULT_DOWNLOAD_DIR
    
    # Create directory if not exists
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
    
    return download_dir


def get_format_options(quality):
    """Get yt-dlp format options based on quality selection."""
    formats = {
        'best': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        '1080p': 'bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080][ext=mp4]/best',
        '720p': 'bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720][ext=mp4]/best',
        '480p': 'bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]/best[height<=480][ext=mp4]/best',
        'audio': 'bestaudio[ext=m4a]/bestaudio/best',
    }
    
    return formats.get(quality, formats['best'])


def download_video(url, output_path, quality):
    """Download video in a background thread with bypass techniques."""
    
    # Base options
    ydl_opts = {
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'format': get_format_options(quality),
        'noplaylist': True,
        'quiet': False,
        'no_warnings': False,
        # Bypass YouTube restrictions
        'extractor_args': {
            'youtube': {
                'player_client': ['android', 'tv_creator'],
                'player_skip': ['webpage', 'configs'],
            }
        },
        # Use browser-like headers
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
        },
        # Retry settings
        'retries': 3,
        'fragment_retries': 3,
    }
    
    # Add post-processing for audio-only
    if quality == 'audio':
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            return {'success': True, 'filename': os.path.basename(filename)}
    except Exception as e:
        return {'success': False, 'error': str(e)}


@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')


@app.route('/download', methods=['POST'])
def download():
    """Handle download request."""
    data = request.get_json()
    
    url = data.get('url', '').strip()
    quality = data.get('quality', 'best')
    output_choice = data.get('output_path', '')
    
    if not url:
        return jsonify({'success': False, 'message': 'Please enter a YouTube URL'})
    
    output_path = get_output_path(output_choice)
    
    # Run download in background thread to avoid timeout
    result_container = {}
    
    def download_thread():
        result_container['result'] = download_video(url, output_path, quality)
    
    thread = threading.Thread(target=download_thread)
    thread.start()
    thread.join()  # Wait for completion
    
    result = result_container.get('result', {})
    
    if result.get('success'):
        return jsonify({
            'success': True, 
            'message': f"Downloaded successfully to: {output_path}"
        })
    else:
        error_msg = result.get('error', 'Unknown error')
        # Handle common errors
        if 'HTTP Error 403' in error_msg:
            error_msg = "YouTube blocked the download. This video may be age-restricted or unavailable. Try a different video."
        elif 'HTTP Error 429' in error_msg:
            error_msg = "Too many requests. Please wait a few minutes and try again."
        elif 'Unable to extract' in error_msg:
            error_msg = "Could not extract video information. The URL may be invalid."
        elif 'Video unavailable' in error_msg:
            error_msg = "This video is unavailable."
        
        return jsonify({'success': False, 'message': error_msg})


if __name__ == '__main__':
    print("=" * 50)
    print("YouTube Video Downloader Web App")
    print("=" * 50)
    print("Open your browser and go to: http://127.0.0.1:5000")
    print("=" * 50)
    app.run(debug=True, host='0.0.0.0', port=5000)
