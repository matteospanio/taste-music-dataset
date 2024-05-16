#!/usr/bin/env bash

source ./logger.sh

URL="https://files.de-1.osf.io/v1/resources/2cqa5/providers/osfstorage/?zip="
SOUNDS_PATH="Taste & Affect Music Database Soundtracks/Taste Affect Music Database_OSF.rar"

# download the taste affective music database if necessary
if [ ! -f /tmp/download.zip ]; then
    info "Download dataset."
    curl "$URL" --output /tmp/download.zip
else
    warn "Using cached dataset."
fi

# extract the soundtracks
unzip -jc /tmp/download.zip "$SOUNDS_PATH" > /tmp/soundtracks.rar

if [ -d soundtracks ]; then
    warn "soundtracks directory already exists."
    if [ -z "$(ls -A soundtracks)" ]; then
        info "soundtracks directory is empty."
    else
        error "soundtracks directory is not empty."
        exit 1
    fi
else
    mkdir soundtracks
    info "soundtracks folder created."
fi

cd soundtracks || exit 1

unrar e /tmp/soundtracks.rar >/dev/null

if [ $? -eq 0 ]; then
    info "Done"
else
    error "An error occurred while extracting soundtracks."
fi
