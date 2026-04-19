from http.server import BaseHTTPRequestHandler
import json
import subprocess
import sys
import os
import tempfile


def install_ytdlp():
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "-q", "yt-dlp"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def get_video_info(url):
    try:
        import yt_dlp
    except ImportError:
        install_ytdlp()
        import yt_dlp

    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
        "noplaylist": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    title = info.get("title", "Facebook Video")
    thumbnail = info.get("thumbnail", "")

    formats = info.get("formats", [])
    qualities = []
    seen = set()

    for f in formats:
        if f.get("vcodec") == "none":
            continue
        height = f.get("height")
        ext = f.get("ext", "mp4")
        furl = f.get("url")
        if not furl or not height:
            continue
        label = f"{height}p"
        if label in seen:
            continue
        seen.add(label)
        fsize = f.get("filesize") or f.get("filesize_approx")
        size_str = f"{round(fsize / 1048576, 1)} MB" if fsize else "MP4 Video"
        vcodec = f.get("vcodec", "")
        tbr = f.get("tbr")
        if tbr:
            size_str = f"{round(tbr)} kbps"
        qualities.append({
            "quality": label,
            "size": size_str,
            "url": furl,
            "ext": ext,
        })

    qualities.sort(key=lambda x: int(x["quality"].replace("p", "")), reverse=True)

    if not qualities:
        raise ValueError("No downloadable video formats found. The video may be private.")

    return {"title": title, "thumbnail": thumbnail, "qualities": qualities}


class handler(BaseHTTPRequestHandler):

    def do_OPTIONS(self):
        self.send_response(200)
        self._cors()
        self.end_headers()

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)

        try:
            data = json.loads(body)
        except Exception:
            self._json(400, {"error": "Invalid JSON."})
            return

        url = data.get("url", "").strip()

        if not url:
            self._json(400, {"error": "Please provide a Facebook video URL."})
            return

        valid = (
            "facebook.com" in url
            or "fb.watch" in url
            or "fb.com" in url
        )
        if not valid:
            self._json(400, {"error": "Please provide a valid Facebook video URL."})
            return

        try:
            result = get_video_info(url)
            self._json(200, result)
        except ValueError as e:
            self._json(404, {"error": str(e)})
        except Exception as e:
            self._json(500, {"error": f"Could not extract video: {str(e)}"})

    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def _json(self, status, payload):
        body = json.dumps(payload).encode()
        self.send_response(status)
        self._cors()
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass
