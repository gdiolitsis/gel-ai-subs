import xbmc
import xbmcaddon
import xbmcgui
import json
import urllib.request

addon = xbmcaddon.Addon()
SERVER = addon.getSetting("server_url")
LANG   = addon.getSetting("language")

def get_subtitles():
    player = xbmc.Player()
    video = player.getPlayingFile()

    if not video:
        return []

    payload = json.dumps({
        "path": video,
        "lang": LANG
    }).encode("utf-8")

    try:
        req = urllib.request.Request(
            SERVER + "/transcribe",
            data=payload,
            headers={"Content-Type": "application/json"}
        )
        res = urllib.request.urlopen(req, timeout=600)
        data = json.loads(res.read().decode("utf-8"))
    except Exception as e:
        xbmc.log(f"GEL AI Subs error: {e}", xbmc.LOGERROR)
        return []

    srt = data.get("srt")
if not srt:
    return []

# Build full URL
if srt.startswith("/"):
    srt_url = SERVER.rstrip("/") + srt
else:
    srt_url = srt

return [{
    "language_name": LANG,
    "language_flag": LANG,
    "filename": srt_url
}]
