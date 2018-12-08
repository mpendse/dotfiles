#! /usr/bin/env python3
import subprocess, shlex, readline, sys, re, os, time

def read():
    return input("")

commands = {
    " " : "PlayPause",
    "p" : "Previous",
    "n" : "Next",
}
dbus_prefix = "dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player."
metadata_cmd = "dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.freedesktop.DBus.Properties.Get string:\"org.mpris.MediaPlayer2.Player\" string:'Metadata'"
# source for this thing : https://gist.github.com/wandernauta/6800547
# grep -Ev "^method" | grep -Eo '("(.*)")|(\b[0-9][a-zA-Z0-9.]*\b)' | sed -E '2~2 a|' | tr -d '\n' | sed -E 's/\|/\n/g' | sed -E 's/(xesam:)|(mpris:)//' | sed -E 's/^"//'  | sed -E 's/"$//' | sed -E 's/"+/|/' | sed -E 's/ +/ /g'

r_title = re.compile(r"string;\"\w+:title\";variant;string;\"(.*?)\";")
r_album = re.compile(r"string;\"\w+:album\";variant;string;\"(.*?)\";")
r_artist = re.compile(r"string;\"\w+:artist\";variant;array;\[;string;\"(.*?)\";")
r_album_artist = re.compile(r"string;\"\w+:albumArtist\";variant;array;\[;string;\"(.*?)\";")

def eval(arg):
    c = commands.get(arg, None)
    if not c:
        os.system("clear")
        get_metadata()
        return "\ncommands = {}".format(commands)
    command = dbus_prefix + c
    subprocess.check_call(shlex.split(command))
    os.system("clear")
    if arg == "p" or arg == "n":
        time.sleep(2)
    get_metadata()
    return ""

def get_metadata():
    try:
        out = subprocess.check_output(shlex.split(metadata_cmd))
    except subprocess.CalledProcessError as e:
        print(e.output)
    else:
        p = ";".join(out.decode("utf-8").replace("\n", "").replace("\r", "").replace("\t", "").split())
        for i in (r_title, r_artist, r_album_artist, r_album):
            m = i.search(p)
            if(m):
                print(m.group(1).replace(";", " "))

def main():
    get_metadata()
    try:
        while True:
            print(eval(read()))
    except (EOFError, KeyboardInterrupt):
        print("")
    finally:
        sys.exit(0)

if __name__ == "__main__":
    main()
