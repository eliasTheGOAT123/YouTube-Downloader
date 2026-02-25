# YouTube Video Downloader
Hi louai
A modern web-based YouTube video downloader with a beautiful dark-themed GUI.

![YouTube Downloader](https://img.shields.io/badge/YouTube-Downloader-red?style=for-the-badge&logo=youtube)
![Python](https://img.shields.io/badge/Python-3.14-blue?style=flat&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.1-white?style=flat&logo=flask)

## Features

- 🎨 **Modern UI** - Beautiful dark theme with smooth animations
- 📺 **Multiple Quality Options** - Best, 1080p, 720p, 480p, Audio (MP3)
- 📁 **Flexible Output** - Save to Downloads, Videos, or Desktop
- 📱 **Responsive Design** - Works on desktop and mobile
- 🔄 **Auto-retry** - Handles connection issues gracefully

## Prerequisites

- Python 3.8 or higher
- Windows, macOS, or Linux

## Installation

1. **Clone or download this repository**
   
```
bash
git clone https://github.com/YOUR_USERNAME/youtube-downloader.git
cd youtube-downloader
```

2. **Install required libraries**
   
```
bash
pip install flask yt-dlp
```

## Usage

1. **Start the web server**
   
```
bash
python app.py
```

2. **Open in browser**
   Navigate to: `http://127.0.0.1:5000`

3. **Download videos**
   - Paste a YouTube URL
   - Select quality (Best, 1080p, 720p, 480p, Audio)
   - Choose output folder
   - Click Download

## Project Structure

```
youtube-downloader/
├── app.py                 # Flask web application
├── templates/
│   └── index.html         # Web UI template
├── README.md              # This file
└── requirements.txt       # Python dependencies
```

## Troubleshooting

### YouTube blocks downloads (403 Error)
- YouTube has anti-bot measures that may block some downloads
- Try:
  - Using a different video
  - Waiting a few minutes between downloads
  - Selecting a lower quality option

### Installation errors
- Make sure Python is in your PATH
- Try: `py -m pip install flask yt-dlp`

### Port already in use
- Kill existing process: `taskkill /F /IM python.exe` (Windows)
- Or change port in app.py: `app.run(port=5001)`

## Technologies Used

- **Backend**: Python, Flask, yt-dlp
- **Frontend**: HTML5, CSS3, JavaScript
- **Design**: Custom dark theme with CSS animations

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This tool is intended for personal use only. Please respect copyright laws and YouTube's terms of service when using this downloader.

---

⭐ Star this repository if it helped you!
