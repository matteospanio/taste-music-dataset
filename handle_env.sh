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

info "Running the script..."
python dataset.py data data/annotations 2>/dev/null

info "Cleaning the environment..."
mkdir -p data/dataset
mv data/soundtracks/* data/dataset
mv data/annotations/* data/dataset
rmdir data/soundtracks
rmdir data/annotations

info "Generating jsonl files..."
python make_jsonl.py data/dataset data

info "Bye!"
deactivate
