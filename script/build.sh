#!/bin/sh
go get github.com/mitchellh/gox
gox --osarch "linux/amd64" --output "/tmp/dist/app_{{.OS}}_{{.Arch}}"
