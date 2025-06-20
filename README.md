# 🎥 YouTube Downloader
A sleek and powerful Flask web app that allows users to download YouTube videos and playlists in various formats, including audio-only. Built with `yt-dlp`, this downloader offers real-time progress tracking, responsive UI, and support for playlists with intelligent search functionality.

![Screenshot 2025-06-19 122619](https://github.com/user-attachments/assets/f58bbe76-0b51-4978-ab46-a1017e8b6ea9)
![Screenshot 2025-06-19 122628](https://github.com/user-attachments/assets/0af4bd4f-8ef9-4517-9cfb-331bcbee51ef)
![Screenshot 2025-06-20 195439](https://github.com/user-attachments/assets/304cf11e-191d-4653-97fd-08c390455534)
![Screenshot 2025-06-20 195511](https://github.com/user-attachments/assets/3bf0e8d6-308e-4041-ab9a-d584bbfc0b30)


## 🚀 Features
- 🔍 **Smart Search**: Search YouTube directly within the app - no need to copy URLs!
- 📋 **Interactive Results**: Browse search results with thumbnails and select videos easily
- 🎞️ **Multiple Formats**: Download videos in various resolutions and formats (MP4, WebM, etc.)
- 🎧 **Audio-Only Support**: Extract audio tracks for music and podcasts
- 📂 **Playlist Support**: Download entire playlists with auto folder creation
- ⚡ **Real-time Progress**: Track download progress with visual progress bars
- 💻 **Responsive UI**: Clean, user-friendly interface that works on all devices
- 📁 **Auto-Save**: Files saved directly to your system's `Downloads` folder
- 🛡️ **Anti-Bot Protection**: Built-in measures to avoid YouTube rate limiting

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

### 4. Setup cookies (Important!)
Create a `cookies.txt` file in the project root directory to avoid YouTube bot detection:
# Get cookies using browser extension like "Get cookies.txt"
# Place the cookies.txt file in the same directory as app.py

## ▶️ Usage
### 1. Run the Flask app
python app.py

### 2. Open in your browser
Navigate to: http://127.0.0.1:5000

### 3. Two ways to download:

#### Method 1: Search and Select 🔍
1. **Enter search terms** (e.g., "lo-fi beats", "tech tutorials", "cooking recipes")
2. **Browse results** with thumbnails and video details
3. **Click "Select"** on your desired video
4. **Choose format** and download

#### Method 2: Direct URL (Traditional)
1. **Paste any YouTube URL** in the search box
2. **Click "Get Video Info"** to fetch details
3. **Select desired format** from the dropdown
4. **Click "Download Selected Format"**

## 🔍 Search Examples
Try searching for:
- "lofi hip hop beats"
- "python tutorials"
- "cooking recipes"
- "travel vlogs"
- "tech reviews"

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
├── cookies.txt                 # YouTube cookies (you need to add this)
├── requirements.txt            # All Python dependencies
└── README.md                   # Project documentation

## ✅ Sample Links
Try with these sample videos:
- https://www.youtube.com/watch?v=BaW_jenozKc (yt-dlp test)
- https://www.youtube.com/watch?v=dQw4w9WgXcQ (Rick Astley)
- https://www.youtube.com/watch?v=21X5lGlDOfg (NASA Live)

## 🎯 Key Improvements
### Search Functionality
- **No more URL hunting**: Search directly within the app
- **Visual browsing**: See thumbnails, titles, and uploaders
- **Quick selection**: One-click video selection from results
- **Smart results**: Up to 10 relevant videos per search

### Enhanced User Experience
- **Loading states**: Visual feedback during processing
- **Error handling**: Clear error messages and troubleshooting
- **Progress tracking**: Real-time download progress bars
- **Responsive design**: Works perfectly on mobile and desktop

## 📌 Notes
- All files are saved in your OS-specific Downloads directory
- Large playlist downloads may take time and show a directory path on success
- Search results are limited to 10 videos for better performance
- If download appears stalled, check your internet connection or try another format
- **cookies.txt file is required** for reliable YouTube access

## 🧩 Troubleshooting
### Common Issues:

❌ **Error: cookies.txt file not found**
→ Create cookies.txt file in the project directory using a browser extension

❌ **Search results not showing**
→ Check your internet connection and ensure cookies.txt is properly formatted

❌ **"Sign in to confirm you're not a bot"**
→ Wait a few minutes and try again, or update your cookies.txt file

❌ **Error: No URL provided**
→ Ensure you've either searched and selected a video or pasted a valid URL

❌ **Error getting video info**
→ Video might be region-locked, private, or age-restricted

❌ **Download file too small or missing**
→ Retry with another format or verify output folder permissions

### Performance Tips:
- Use search for discovering new content
- Paste URLs directly for known videos
- Choose appropriate quality based on your needs
- Be patient with large playlists

## 📝 License
This project is licensed under the MIT License.

## 💡 Inspiration
Built to simplify the YouTube download experience with a clean interface, intelligent search capabilities, and reliable backend using the power of yt-dlp. Whether you're looking for specific content or exploring new videos, this downloader makes it easy and efficient.

## 👨‍💻 Author
**Yuji Itaori**
GitHub Profile → https://github.com/YujiItaori

---
⭐ **Star this repository if you find it helpful!** ⭐
