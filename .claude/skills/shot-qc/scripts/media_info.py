"""ffprobe media_info() used by hyperkut_export_qc.py. Original stdlib shim, this collection (MIT);
same return keys as HyperKut-Studio backend/media.py media_info (MIT)."""
import json, shutil, subprocess


def media_info(path):
    r = subprocess.run([shutil.which("ffprobe") or "ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)], capture_output=True, timeout=30)
    if r.returncode: raise ValueError("The media could not be decoded")
    d = json.loads(r.stdout); st = d.get("streams", [])
    v = next((s for s in st if s.get("codec_type") == "video" and not s.get("disposition", {}).get("attached_pic")), None)
    a = any(s.get("codec_type") == "audio" for s in st)
    return {"kind": "video" if v else "audio", "has_audio": a,
            "video_duration": float((v or {}).get("duration") or d.get("format", {}).get("duration") or 0),
            "duration": float(d.get("format", {}).get("duration") or (v or {}).get("duration") or 0),
            "width": int((v or {}).get("width", 0)), "height": int((v or {}).get("height", 0)),
            "fps": (v or {}).get("avg_frame_rate", "0/1")}
