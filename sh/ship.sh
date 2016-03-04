#!/bin/sh
SHIP_PREFIX="$1"

SHIP_TAG=$SHIP_PREFIX`cat release_tag`
SHIP_USER="bluele"
SHIP_REPO="go-nginx-docker"
TARGET_ARCH="linux_amd64"
APP_NAME="app_$TARGET_ARCH"
DIST_PATH="./dist/$APP_NAME"

docker-compose up build
go get github.com/aktau/github-release
github-release release --user $SHIP_USER --repo $SHIP_REPO --tag $SHIP_TAG --name $APP_NAME --description "sample"
github-release upload --user $SHIP_USER --repo $SHIP_REPO --tag $SHIP_TAG --name $APP_NAME --file $DIST_PATH
