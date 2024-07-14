#!/usr/bin/env bash
VENV=".venv"

source ./logger.sh

if [ -d "$VENV" ]; then
    info "Activating virtual environment..."
    # shellcheck source=.venv/bin/activate
    source "$VENV/bin/activate"
else
    warn "No virtual environment found."
    info "Creating virtual environment..."
    python3 -m venv "$VENV"
    # shellcheck source=.venv/bin/activate
    source "$VENV/bin/activate"
fi

info "Installing dependencies..."
pip install -r requirements.txt

info "Bye!"
deactivate
