#!/usr/bin/env bash
query=$1
audio_path="/Users/pmz/Library/Mobile Documents/com~apple~CloudDocs/Alfred/Alfred.alfredpreferences/dict_audio"
target_path="$audio_path/$query.mp3"
url="https://howjsay.com/mp3/$query.mp3"
if [ ! -f "$target_path" ]; then
    /usr/local/bin/wget --connect-timeout=3 -O "$target_path" "$url"
    if [ $? -eq 0 ]; then
        echo "NOT EXIST"
        echo "ADDED"
        afplay "$audio_path/$query.mp3"
    else
        echo "CONNECTION ERROR"
        rm "$target_path"
        say "Connection Error"
    fi
else
    echo "EXIST"
    afplay "$audio_path/$query.mp3"
fi
