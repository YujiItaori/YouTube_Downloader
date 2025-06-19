# 🎥 YouTube Downloader

A sleek and powerful Flask web app that allows users to download YouTube videos and playlists in various formats, including audio-only. Built with `yt-dlp`, this downloader offers real-time progress tracking, responsive UI, and support for playlists.

![Screenshot 2025-06-19 122619](https://github.com/user-attachments/assets/f58bbe76-0b51-4978-ab46-a1017e8b6ea9)
![Screenshot 2025-06-19 122628](https://github.com/user-attachments/assets/0af4bd4f-8ef9-4517-9cfb-331bcbee51ef)


## 🚀 Features

- 🔍 Fetch video information before downloading
  
- 🎞️ Download videos in various resolutions and formats (MP4, WebM, etc.)

- 🎧 Audio-only download support

- 📂 Playlist support with auto folder creation

- 💻 User-friendly responsive UI

- 📁 Files saved directly to your system's `Downloads` folder


## 🛠️ Tech Stack

- **Frontend:** HTML5, CSS, Font Awesome

- **Backend:** Python, Flask

- **Downloader:** [yt-dlp](https://github.com/yt-dlp/yt-dlp)


## 📦 Installation

### 1. Clone the repository

git clone https://github.com/YujiItaori/YouTube_Downloader.git

cd YouTube_Downloader

### 2. Create a virtual environment

python -m venv youtube_env

source youtube_env/bin/activate  # On Windows use: youtube_env\Scripts\activate

### 3. Install dependencies

pip install -r requirements.txt

## ▶️ Usage

### 1. Run the Flask app

python app.py

### 2. Open in your browser

Navigate to: http://127.0.0.1:5000

### 3. Paste any YouTube URL and:

Click "Get Video Info" to fetch details.

Select desired format.

Click "Download Selected Format".

## 📂 Folder Structure

YouTube_Downloader/
│
├── static/
│   └── style.css               # Custom CSS styles
│
├── templates/
│   └── index.html              # Jinja2 template for frontend
│
├── app.py                      # Main Flask backend logic
├── requirements.txt            # All Python dependencies
└── README.md                   # Project documentation

## ✅ Sample Links

Try with these sample videos:

https://www.youtube.com/watch?v=BaW_jenozKc (yt-dlp test)

https://www.youtube.com/watch?v=dQw4w9WgXcQ (Rick Astley)

https://www.youtube.com/watch?v=21X5lGlDOfg (NASA Live)

## 📌 Notes

All files are saved in your OS-specific Downloads directory.

Large playlist downloads may take time and show a directory path on success.

If download appears stalled, check your internet connection or try another format.

## 🧩 Troubleshooting

❌ Error: No URL provided
→ Ensure the URL input is filled.

❌ Error getting video info
→ Video might be region-locked or private.

❌ Download file too small or missing
→ Retry with another format or verify output folder permissions.

## 📝 License

This project is licensed under the MIT License.

## 💡 Inspiration

Built to simplify the YouTube download experience with a clean interface and reliable backend using the power of yt-dlp.

👨‍💻 Author

Yuji Itaori

GitHub Profile → https://github.com/YujiItaori
