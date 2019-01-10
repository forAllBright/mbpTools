#!/usr/bin/env bash
query=$1
url="https://howjsay.com/mp3/$query.mp3"
/usr/local/bin/wget -O "audio/$query.mp3" $url
afplay "audio/$query.mp3"