#!/bin/sh
python script/image-update.py check --files $WATCH_FILES --cache ~/cache/digests --debug
if [ "$?" -eq 0 ]
then
    python script/docker-cache.py load --cache ~/cache/images --debug
else
    mkdir -p ~/cache/images
    mkdir -p ~/cache/digests
    docker-compose build
    python script/docker-cache.py save --cache ~/cache/images --debug
    python script/image-update.py save --files $WATCH_FILES --cache ~/cache/digests --debug
fi
