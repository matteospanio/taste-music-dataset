#!/usr/bin/env python3
from __future__ import annotations
import argparse as ap
from dataclasses import dataclass, asdict
import json
import pathlib as pl
import pandas as pd
import numpy as np
import librosa
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3

COLUMNS = [
    "Sweet",
    "Bitter",
    "Sour",
    "Salty",
    "Joy",
    "Sadness",
    "Surprise",
    "Fear",
    "Anger",
    "Valence (P)",
    "Arousal (P)",
    "Familiarity",
    "Valence (F)",
    "Arousal (F)",
]


@dataclass(frozen=True)
class Metadata:
    key: str
    artist: str
    sample_rate: int
    file_extension: str
    description: str
    keywords: str
    duration: float
    bpm: str
    genre: str
    title: str
    name: str
    instrument: str
    moods: list[str]

    @classmethod
    def from_file(cls, file: pl.Path, kw: list[str]) -> Metadata:
        s = MP3(file, ID3=EasyID3)

        with open("descriptions.json") as f:
            descriptions = json.load(f)

        dd = descriptions[int(file.stem) - 1]

        try:
            bpm = s["bpm"][0]
        except KeyError:
            y, sr = librosa.load(file, sr=None)
            bpm = round(librosa.feature.tempo(y=y, sr=sr).mean())

        return cls(
            key=get_key(file),
            artist=s["artist"][0],
            sample_rate=int(s.info.sample_rate),
            file_extension=file.suffix,
            description=dd["description"],
            keywords=", ".join(kw),
            duration=float(s.info.length),
            bpm=str(bpm),
            genre=s["genre"][0],
            title=s["title"][0],
            name=file.stem,
            instrument=dd["instrument"],
            moods=str(s["grouping"][0]).split(", "),
        )


def get_key(song: pl.Path) -> str:
    y, sr = librosa.load(song, sr=None)
    chroma = librosa.feature.chroma_cqt(y=y, sr=sr)

    # Compute the mean chroma over time
    chroma_mean = np.mean(chroma, axis=1)

    key_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

    # Find the index of the maximum mean chroma value
    key_index = chroma_mean.argmax()

    key = key_names[key_index]

    return key


def get_keywords(song: pl.Path, df: pd.DataFrame) -> list[str]:
    keywords = []
    row = df.loc[int(song.stem)]
    kw = np.array([row["Sweet"], row["Bitter"], row["Sour"], row["Salty"]])

    for i, k in enumerate(kw):
        if k > 25:
            match i:
                case 0:
                    keywords += ["Sweet"]
                case 1:
                    keywords += ["Bitter"]
                case 2:
                    keywords += ["Sour"]
                case 3:
                    keywords += ["Salty"]
                case _:
                    keywords += []

    return keywords


def main():
    parser = ap.ArgumentParser(
        description="Create metadata files for all the songs in the dataset"
    )
    parser.add_argument("source", type=str, help="Source folder", metavar="SRC")
    parser.add_argument(
        "destination", type=str, help="Destination folder", metavar="DST"
    )

    args = parser.parse_args()

    src = pl.Path(args.source)
    dst = pl.Path(args.destination)
    if not dst.exists():
        dst.mkdir()

    data = src / "metadata_2.xlsx"
    df = pd.read_excel(data)
    df = df.loc[:, COLUMNS]

    for song in sorted(src.glob("**/*.mp3")):
        keywords = get_keywords(song, df)
        with (dst / f"{song.stem}.json").open("w") as f:
            json.dump(asdict(Metadata.from_file(song, keywords)), f, indent=4)


if __name__ == "__main__":
    main()
