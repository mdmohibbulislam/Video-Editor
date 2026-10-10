# Video Editor

A simple web-based video editor built with **Django** and **FFmpeg**.

Upload videos and perform common editing tasks directly from the browser.

## Features

- Upload videos
- Trim video (start time + duration)
- Add text overlay
- Generate thumbnail
- Change playback speed
- Merge two videos
- Edit title / replace original file
- Delete videos
- Download processed results

## Tech Stack

- Python & Django
- FFmpeg
- SQLite (default)

## Requirements

- Python 3.10+
- Django 5+ / 6
- FFmpeg installed and available in system PATH

## Setup

```bash
# Clone the repository
git clone https://github.com/mdmohibbulislam/Video-Editor.git
cd Video-Editor

# Create virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# Install dependencies
pip install django

# Run migrations
python manage.py migrate

# Start the server
python manage.py runserver
```
Open http://127.0.0.1:8000 in your browser.

## Notes

- Uploaded and processed files are stored in the media/ folder (ignored by Git).
- Make sure FFmpeg is installed (ffmpeg -version).
- Change the SECRET_KEY in settings.py before deploying to production.

## License

This project is open source and available under the MIT License.
text---

```
After updating the file, commit and push:
```
```powershell
git add README.md
git commit -m "Update README"
git push
```
