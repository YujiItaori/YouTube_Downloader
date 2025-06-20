from flask import Flask, render_template, request, send_file, jsonify
import yt_dlp
import os
from pathlib import Path
import time
import random

app = Flask(__name__)

DOWNLOAD_FOLDER = str(Path.home() / "Downloads")
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

SAMPLE_VIDEOS = {
    "Test Video (yt-dlp official)": "https://www.youtube.com/watch?v=BaW_jenozKc",
    "Rick Astley - Never Gonna Give You Up": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "NASA Live": "https://www.youtube.com/watch?v=21X5lGlDOfg"
}

# Global dictionary to store download progress
download_progress = {}

def get_ydl_opts(progress_hook=None, output_template=None):
    """Get yt-dlp options with anti-bot measures"""
    # Get the directory where app.py is located
    app_dir = os.path.dirname(os.path.abspath(__file__))
    cookies_path = os.path.join(app_dir, 'cookies.txt')
    
    opts = {
        'quiet': True,
        'no_warnings': True,
        # Use cookies file for authentication
        'cookiefile': cookies_path,
        # Anti-bot measures
        'sleep_interval': random.uniform(1, 3),
        'max_sleep_interval': 5,
        'sleep_interval_requests': random.uniform(1, 3),
        'sleep_interval_subtitles': random.uniform(1, 3),
        # User agent rotation
        'http_headers': {
            'User-Agent': random.choice([
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            ])
        },
        # Additional options to bypass restrictions
        'extractor_retries': 3,
        'fragment_retries': 3,
        'skip_unavailable_fragments': True,
        # Additional YouTube-specific options
        'youtube_include_dash_manifest': False,
    }
    
    if progress_hook:
        opts['progress_hooks'] = [progress_hook]
    
    if output_template:
        opts['outtmpl'] = output_template
        opts['merge_output_format'] = 'mp4'
    
    return opts

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        step = request.form.get('step')
        video_url = request.form.get('custom_url') or request.form.get('sample_url')

        if step != "search":
            video_url = request.form.get('custom_url') or request.form.get('sample_url')
            if not video_url:
                return "❌ Error: No URL provided."
        else:
            video_url = None

        # Add delay to avoid being detected as bot
        time.sleep(random.uniform(1, 2))

        if step == "info":
            try:
                opts = get_ydl_opts()
                opts['skip_download'] = True
                
                # Check if cookies file exists
                app_dir = os.path.dirname(os.path.abspath(__file__))
                cookies_path = os.path.join(app_dir, 'cookies.txt')
                if not os.path.exists(cookies_path):
                    return render_template('index.html', 
                                         samples=SAMPLE_VIDEOS, 
                                         error="cookies.txt file not found. Please ensure it's in the same directory as app.py")
                
                with yt_dlp.YoutubeDL(opts) as ydl:
                    info_dict = ydl.extract_info(video_url, download=False)

                    if info_dict.get('_type') == 'playlist':
                        return render_template('index.html', samples=SAMPLE_VIDEOS, playlist_title=info_dict.get('title'), playlist=True, selected_url=video_url)

                    formats = [
                        {
                            'format_id': f['format_id'],
                            'ext': f['ext'],
                            'resolution': f.get('format_note') or f.get('height') or 'audio',
                            'filesize': round((f.get('filesize') or 0) / 1_048_576, 2),
                            'vcodec': f.get('vcodec', '')
                        }
                        for f in info_dict['formats']
                        if f.get('filesize')
                    ]

                    return render_template('index.html', samples=SAMPLE_VIDEOS, info=info_dict, formats=formats, selected_url=video_url)

            except Exception as e:
                error_msg = str(e)
                if "Sign in to confirm you're not a bot" in error_msg:
                    return render_template('index.html', 
                                         samples=SAMPLE_VIDEOS, 
                                         error="YouTube is blocking automated downloads. Try again in a few minutes or use a different video.")
                return f"❌ Error getting video info: {error_msg}"
        
        elif step == "search":
            search_query = request.form.get('search_query')
            if not search_query:
                return render_template('index.html', samples=SAMPLE_VIDEOS, error="Search query is empty.")

            try:
                search_opts = get_ydl_opts()
                search_opts['quiet'] = True
                search_opts['skip_download'] = True
                search_opts['extract_flat'] = True  # THIS IS CRUCIAL!
                
                # Format the search query properly
                formatted_query = f"ytsearch10:{search_query}"

                with yt_dlp.YoutubeDL(search_opts) as ydl:
                    search_result = ydl.extract_info(formatted_query, download=False)

                # Debug print to see what we're getting
                print(f"DEBUG: Search result type: {type(search_result)}")
                print(f"DEBUG: Search result keys: {search_result.keys() if isinstance(search_result, dict) else 'Not a dict'}")
                
                if search_result and 'entries' in search_result:
                    entries = search_result['entries']
                    print(f"DEBUG: Found {len(entries)} entries")
                    
                    # Process entries to ensure they have the required fields
                    processed_entries = []
                    for entry in entries:
                        if entry:  # Skip None entries
                            # Ensure each entry has the required fields
                            processed_entry = {
                                'title': entry.get('title', 'Unknown Title'),
                                'url': entry.get('url', entry.get('webpage_url', '')),
                                'uploader': entry.get('uploader', entry.get('channel', 'Unknown')),
                                'thumbnails': entry.get('thumbnails', []),
                                'id': entry.get('id', ''),
                                'duration': entry.get('duration', 0)
                            }
                            processed_entries.append(processed_entry)
                    
                    return render_template('index.html', 
                                        samples=SAMPLE_VIDEOS, 
                                        search_results=processed_entries)
                else:
                    return render_template('index.html', 
                                        samples=SAMPLE_VIDEOS, 
                                        error="No search results found.")

            except Exception as e:
                print(f"DEBUG: Search error: {str(e)}")
                return render_template('index.html', 
                                    samples=SAMPLE_VIDEOS, 
                                    error=f"Search failed: {str(e)}")


        elif step == "download":
            format_id = request.form.get('format_id')
            video_id = request.form.get('video_id')
            video_url = request.form.get('custom_url')

            def progress_hook(d):
                if not video_id:
                    return
                if d['status'] == 'downloading':
                    download_progress[video_id] = {
                        'status': 'downloading',
                        'downloaded_bytes': d.get('downloaded_bytes', 0),
                        'total_bytes': d.get('total_bytes', d.get('total_bytes_estimate', 1))
                    }
                elif d['status'] == 'finished':
                    download_progress[video_id] = {'status': 'finished'}

            try:
                # Check if cookies file exists
                app_dir = os.path.dirname(os.path.abspath(__file__))
                cookies_path = os.path.join(app_dir, 'cookies.txt')
                if not os.path.exists(cookies_path):
                    return "❌ Error: cookies.txt file not found. Please ensure it's in the same directory as app.py"
                
                # First get info
                info_opts = get_ydl_opts()
                info_opts['skip_download'] = True
                
                with yt_dlp.YoutubeDL(info_opts) as ydl:
                    info_dict = ydl.extract_info(video_url, download=False)

                # Add delay between requests
                time.sleep(random.uniform(2, 4))

                if info_dict.get('_type') == 'playlist':
                    playlist_title = info_dict.get('title', 'Playlist')
                    playlist_folder = os.path.join(DOWNLOAD_FOLDER, ''.join(c for c in playlist_title if c.isalnum() or c in (' ', '_', '-')).rstrip())
                    os.makedirs(playlist_folder, exist_ok=True)

                    for i, entry in enumerate(info_dict['entries']):
                        if entry is None:
                            continue
                        
                        # Add delay between playlist items
                        if i > 0:
                            time.sleep(random.uniform(3, 6))
                            
                        video_title = entry.get('title', 'video').strip()
                        safe_title = ''.join(c for c in video_title if c.isalnum() or c in (' ', '_', '-')).rstrip()
                        output_path_template = os.path.join(playlist_folder, safe_title + ".%(ext)s")

                        ydl_opts = get_ydl_opts(progress_hook, output_path_template)
                        ydl_opts['format'] = f"{format_id}+bestaudio/best" if format_id else "best"
                        ydl_opts['noplaylist'] = True

                        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                            ydl.download([entry['webpage_url']])

                    return f"✅ Playlist '{playlist_title}' downloaded to: {playlist_folder}"

                # Single video download
                video_title = info_dict.get('title', 'video').strip()
                safe_title = ''.join(c for c in video_title if c.isalnum() or c in (' ', '_', '-')).rstrip()
                output_path_template = os.path.join(DOWNLOAD_FOLDER, safe_title + ".%(ext)s")
                final_path = os.path.join(DOWNLOAD_FOLDER, safe_title + ".mp4")

                ydl_opts = get_ydl_opts(progress_hook, output_path_template)
                ydl_opts['format'] = f"{format_id}+bestaudio/best" if format_id else "best"
                ydl_opts['noplaylist'] = True

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info_dict = ydl.extract_info(video_url, download=True)
                    downloaded_ext = info_dict.get('ext', 'mp4')
                    alt_path = os.path.join(DOWNLOAD_FOLDER, f"{safe_title}.{downloaded_ext}")

                    if os.path.exists(alt_path) and alt_path != final_path:
                        os.rename(alt_path, final_path)

                    if not os.path.exists(final_path) or os.path.getsize(final_path) < 1000:
                        return "❌ Error: Downloaded file is too small or missing."

                    return send_file(final_path, as_attachment=True, download_name=os.path.basename(final_path))

            except Exception as e:
                error_msg = str(e)
                if "Sign in to confirm you're not a bot" in error_msg:
                    return "❌ YouTube is blocking downloads. Please wait a few minutes and try again, or try a different video."
                return f"❌ Download Error: {error_msg}"

    return render_template('index.html', samples=SAMPLE_VIDEOS)


@app.route('/progress/<video_id>')
def get_progress(video_id):
    return jsonify(download_progress.get(video_id, {
        'status': 'not_found',
        'downloaded_bytes': 0,
        'total_bytes': 1
    }))


if __name__ == '__main__':
    app.run(debug=True)
