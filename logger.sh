#!/usr/bin/env bash

RESET="\033[0m"
RED="\033[31m"
GREEN="\033[32m"
YELLOW="\033[33m"
BLUE="\033[34m"

log () {
    local level="$1"
    local msg="$2"
    local col="$3"
    timestamp=$(date +"%Y-%m-%d %H:%M:%S")
    echo -e "${col}${timestamp} | ${level}\t| ${msg}${RESET}"
}

info () {
    log "INFO" "$1" "$BLUE"
}

error () {
    log "ERROR" "$1" "$RED"
}

warn () {
    log "WARN" "$1" "$YELLOW"
}

success () {
    log "SUCCESS" "$1" "$GREEN"
}
