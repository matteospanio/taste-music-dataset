#!/usr/bin/env python3
from __future__ import annotations
from dataclasses import dataclass
import pathlib as pl
import pandas as pd
import json
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
from pprint import pprint


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
    def from_file(cls, file: pl.Path) -> "Metadata":
        s = MP3(file, ID3=EasyID3)
        return cls(
            key="",
            artist=s["artist"][0],
            sample_rate=int(s.info.sample_rate),
            file_extension=file.suffix,
            description="",
            keywords="",
            duration=float(s.info.length),
            bpm=str(s["bpm"][0]),
            genre=s["genre"][0],
            title=s["title"][0],
            name=file.stem,
            instrument="",
            moods=[],
        )


DATA_PATH = pl.Path("data")
NAMES = DATA_PATH / "metadata_1.xlsx"
DATA = DATA_PATH / "metadata_2.xlsx"

datas = pd.read_excel(DATA)
names = pd.read_excel(NAMES)


def make_meatadata(dst: pl.Path):
    for i, song in enumerate(DATA_PATH.glob("**/*.mp3")):
        if i == 0:
            pprint(Metadata.from_file(song))


# print(names["Title"], names["Author"])
make_meatadata(DATA_PATH)
