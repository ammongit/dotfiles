from constants import PIANOBAR_NOWPLAYING
import subprocess


def audio_player():
    try:
        return subprocess.check_output(("/usr/local/scripts/wm/media/detect-audio-player.sh",))
    except subprocess.CalledProcessError:
        return "??"


def now_playing():
    player = audio_player()
    if player == b"mocp":
        try:
            return subprocess.check_output(("mocp", "-Q", "%song by %artist"))
        except subprocess.CalledProcessError:
            return "(error)"
    elif player == b"pianobar":
        artist = "??"
        title = "??"

        try:
            with open(PIANOBAR_NOWPLAYING, 'r') as fh:
                for line in fh.readlines():
                    if line.startswith("artist="):
                        artist = line[7:-1]
                    elif line.startswith("title="):
                        title = line[6:-1]
        except (FileNotFoundError, IOError, OSError):
            return "(error)"

        return "%s by %s" % (title, artist)
    elif player == b"vlc":
        try:
            output = subprocess.check_output((
                "qdbus", "org.mpris.MediaPlayer2.vlc",
                "/org/mpris/MediaPlayer2", "org.freedesktop.DBus.Properties.Get",
                "org.mpris.MediaPlayer2.Player", "Metadata"))

            for line in output.splitlines():
                if line.startswith("xesam: url: "):
                    return line[12:]

            return "??"
        except subprocess.CalledProcessError:
            return "(error)"
    else:
        return "(none)"


def is_muted():
    return subprocess.getoutput("pamixer --get-mute") == "true"


def get_volume():
    volume = subprocess.getoutput("pamixer --get-volume")

    if volume.isdigit():
        return "%s%%" % (volume,)
    else:
        return "??"
