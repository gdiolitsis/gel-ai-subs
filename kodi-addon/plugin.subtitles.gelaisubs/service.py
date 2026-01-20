import xbmc
import xbmcaddon
import json
import urllib.request
import time

addon = xbmcaddon.Addon()
SERVER = addon.getSetting("server_url")
LANG   = addon.getSetting("language")
AUTO   = addon.getSettingBool("auto_generate")

class Monitor(xbmc.Monitor):
    def onPlayBackStarted(self):
        if not AUTO:
            return

        player = xbmc.Player()
        video = player.getPlayingFile()
        if not video:
            return

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
            urllib.request.urlopen(req, timeout=600)
        except Exception as e:
            xbmc.log(f"GEL AI Subs service error: {e}", xbmc.LOGERROR)

monitor = Monitor()
while not monitor.abortRequested():
    time.sleep(1)
