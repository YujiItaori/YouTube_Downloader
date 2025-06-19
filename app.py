from flask import Flask, render_template, request, send_file, jsonify
import yt_dlp
import os
from pathlib import Path

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

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        step = request.form.get('step')
        video_url = request.form.get('custom_url') or request.form.get('sample_url')

        if not video_url:
            return "❌ Error: No URL provided."

        if step == "info":
            try:
                with yt_dlp.YoutubeDL({'quiet': True, 'skip_download': True}) as ydl:
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
                return f"❌ Error getting video info: {str(e)}"

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
                with yt_dlp.YoutubeDL({'quiet': True, 'skip_download': True}) as ydl:
                    info_dict = ydl.extract_info(video_url, download=False)

                if info_dict.get('_type') == 'playlist':
                    playlist_title = info_dict.get('title', 'Playlist')
                    playlist_folder = os.path.join(DOWNLOAD_FOLDER, ''.join(c for c in playlist_title if c.isalnum() or c in (' ', '_', '-')).rstrip())
                    os.makedirs(playlist_folder, exist_ok=True)

                    for entry in info_dict['entries']:
                        if entry is None:
                            continue
                        video_title = entry.get('title', 'video').strip()
                        safe_title = ''.join(c for c in video_title if c.isalnum() or c in (' ', '_', '-')).rstrip()
                        output_path_template = os.path.join(playlist_folder, safe_title + ".%(ext)s")

                        ydl_opts = {
                            'outtmpl': output_path_template,
                            'format': f"{format_id}+bestaudio/best" if format_id else "best",
                            'merge_output_format': 'mp4',
                            'progress_hooks': [progress_hook],
                            'noplaylist': True
                        }

                        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                            ydl.download([entry['webpage_url']])

                    return f"✅ Playlist '{playlist_title}' downloaded to: {playlist_folder}"

                # Else single video
                video_title = info_dict.get('title', 'video').strip()
                safe_title = ''.join(c for c in video_title if c.isalnum() or c in (' ', '_', '-')).rstrip()
                output_path_template = os.path.join(DOWNLOAD_FOLDER, safe_title + ".%(ext)s")
                final_path = os.path.join(DOWNLOAD_FOLDER, safe_title + ".mp4")

                ydl_opts = {
                    'outtmpl': output_path_template,
                    'format': f"{format_id}+bestaudio/best" if format_id else "best",
                    'merge_output_format': 'mp4',
                    'noplaylist': True,
                    'progress_hooks': [progress_hook]
                }

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
                return f"❌ Download Error: {str(e)}"

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
