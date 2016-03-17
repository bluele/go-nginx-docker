#!/bin/sh
python script/image-update.py check --files $WATCH_FILES --debug
if [ "$?" -eq 0 ]
then
    python script/docker-cache.py load --cache ~/cache --debug
else
    mkdir -p ~/cache
    docker-compose build
    python script/docker-cache.py save --cache ~/cache --debug
    python script/image-update.py save --files $WATCH_FILES --debug
fi
