#!/usr/bin/env bash

# shellcheck disable=SC1091
source ./logger.sh

URL="https://files.de-1.osf.io/v1/resources/2cqa5/providers/osfstorage/?zip="
SOUNDS_PATH="Taste & Affect Music Database Soundtracks/Taste Affect Music Database_OSF.rar"
DOWNLOAD_PATH="/tmp/download.zip"

# download the taste affective music database if necessary
download () {
    if [ ! -f /tmp/download.zip ]; then
        info "Downloading dataset..."
        curl "$URL" --output /tmp/download.zip
    else
        warn "Using cached dataset."
    fi
}

# extract the soundtracks
extract_sounds () {
    info "Extracting soundtracks..."
    unzip -jc "$DOWNLOAD_PATH" "$SOUNDS_PATH" > /tmp/soundtracks.rar

    if [ -d soundtracks ]; then
        warn "soundtracks directory already exists."
        if [ -z "$(ls -A soundtracks)" ]; then
            info "soundtracks directory is empty."
        else
            warn "soundtracks directory is not empty. Skipping sounds extraction."
            return 0
        fi
    else
        mkdir soundtracks
    fi

    cd soundtracks ||  exit 1

    if ! unrar e /tmp/soundtracks.rar >/dev/null; then
        error "An error occurred while extracting soundtracks."
    fi

    cd ..
}

extract_metadata () {
    info "Extracting metadata files..."

    # Get the list of xlsx files in the zip archive
    IFS=$'\n' read -d '' -r -a files \
        < <(unzip -l "$DOWNLOAD_PATH" \
        | grep xlsx \
        | sed -n 's/.*\(Supp_File.*$\)/\1/p')

    # Extract and rename each file
    local index=0
    for file in "${files[@]}"; do
        ((index++))

        if unzip -p "$DOWNLOAD_PATH" "$file" > "metadata_$index.xlsx"; then
            info "Extracted '$file'"
        else
            error "An error occurred while extracting $file"
            exit 1
        fi
    done

}

case $1 in
    "all")
        download
        extract_sounds
        extract_metadata
        mkdir -p data
        mv soundtracks metadata_* data
        ;;
    "sound")
        download
        extract_sounds
        ;;
    "metadata")
        download
        extract_metadata
        ;;
    *)
        echo "Usage: $0 [all|sound|metadata]"
        exit 1
        ;;
esac

success "Done!"
