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
    def from_file(cls, file: pl.Path) -> Metadata:
        s = MP3(file, ID3=EasyID3)

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
            description="",
            keywords="",
            duration=float(s.info.length),
            bpm=str(bpm),
            genre=s["genre"][0],
            title=s["title"][0],
            name=file.stem,
            instrument="",
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


def generate_descriptions():
    desc = [
        ("piano", "A sweet melancholic piano piece."),
        ("piano and strings", "A bitter-sweet dreamy piano piece."),
        (
            "piano",
            "A sweet-salty piece with a continuous arpeggio of short notes. The music is in 3/4 time.",
        ),
        (
            "plucked strings",
            "A bitter piece, a little salty. This is mainly the introduction of the song. Firstly the main melody is played by a plucked string, and at the end starts playing a violin.",
        ),
        ("piano", "A sweet-bitter static piano piece. Really slow tempo."),
        (
            "piano and strings",
            "A bitter-sour piece with high and continuous string notes.",
        ),
        ("strings", "A quite bitter and dissonant piece. Slow tempo."),
        ("harp", "A sweet piece with a harp playing a continuous high melody."),
        (
            "choir",
            "A solemn and bitter piece with a choir singing. Reminds of a requiem.",
        ),
        (
            "electronic",
            "A rythmic and salty piece with a lot of electronic short sounds.",
        ),
        (
            "electric guitar",
            "A bitter and melancholic guitar piece. The guitar is playing a ripetitive riff.",
        ),
        (
            "electronic",
            "A sour and really caotic piece with a lot of electronic sounds.",
        ),
        (
            "strings",
            "A bitter piece with a really low and ininterrpted pedal note and a peaceful melody sang by a choir.",
        ),
        (
            "guitar",
            "A quite bitter and little sweet piece with a guitar playing a sad melody.",
        ),
        (
            "electric guitar",
            "A sweet and salty piece with a guitar playing a continuous arpeggio.",
        ),
        (
            "carion",
            "A really high melody played by a carion. The piece is sweet and a little creepy.",
        ),
        (
            "electronic",
            "A bitter and salty harmonic piece. The piece is really slow with a series of harmonic cadences.",
        ),
        ("strings", "A sweet, consonant piece. The tempo is slow and peaceful."),
        (
            "strings",
            "A bitter and sad piece. There isn't a melody but a series of chords.",
        ),
        (
            "guitar",
            "A bitter-salty piece with a guitar playing a sad arpeggio and melody. A little arabic harmonies.",
        ),
        ("violin", "A bitter and sad piece with a violin playing an endless arpeggio."),
        (
            "piano",
            "A bitter and sad piece played by a piano. The tempo is slow but the accompaniment is continuous and forms a musical carpet for the melody.",
        ),
        (
            "piano and strings",
            "A sweet and bitter piece, a little sad. The piano plays a melody and the strings play a continuous arpeggio.",
        ),
        (
            "piano",
            "A bitter-salty piano piece. The piano plays a melody over a continuous arpeggio.",
        ),
        (
            "strings",
            "A bitter and melancholic piece. The strings play a dramatic melody.",
        ),
        (
            "piano and strings",
            "A bitter and dark piece. A really low melody creates a dark atmosphere.",
        ),
        (
            "piano and strings",
            "A salty and rythmic piece. The strings play fast notes while the piano add some chords in the background.",
        ),
        (
            "electronic",
            "A bitter-sour and rythmic piece. The piece is fast with percussive electronic sounds.",
        ),
        (
            "electronic",
            "A bitter and sour piece. The tempo is slow. Low sounds create a suspense atmosphere.",
        ),
        (
            "strings",
            "A bitter and sour piece. The tempo is slow. The strings play a melody, but the harmony is dissonant and low.",
        ),
        (
            "strings",
            "A salty and rythmic piece. The strings play a fast and rythmic melody that generates an energetic effect.",
        ),
        (
            "electronic",
            "A bitter and sour piece. The tempo is quite static. The piece generates tension and anxiety.",
        ),
        (
            "electric guitar and drums",
            "A sour and rythmic piece. The guitar plays a melody and the drums play a rythmic accompaniment. In the background there is a fast and continuos arpeggio with short notes.",
        ),
        (
            "strings",
            "A bitter and sour piece. The strings play a fast melody with a lot of dissonances.",
        ),
        (
            "strings",
            "A bitter and sour piece. The strings play a low ostinato. After a while begins an high melody by a violin that creates a contrast.",
        ),
        (
            "electronic",
            "A bitter and sour piece. There is no tempo, only a series of low dissonant sounds with an high continuous note in the background.",
        ),
        (
            "electronic",
            "A bitter and sour piece. The tempo is slow. There is a low and continuous percussive sound in the background.",
        ),
        (
            "electronic",
            "A bitter and sour piece. The tempo is slow. Really high and dissonant sounds are played over a simple arpeggio.",
        ),
        (
            "electronic",
            "A bitter and sour piece. The tempo is slow. A high continuous dissonant note is played in the background. Low sounds interrupt the high note.",
        ),
        (
            "electronic",
            "A bitter and sour piece. The tempo is concitato. The piece is dissonant and there is a continuous percussive low sound.",
        ),
        (
            "electronic",
            "A sour and bitter piece. Slow tempo. A high short sound is played over a low and continuous sound.",
        ),
        (
            "electronic",
            "A sour and a little bitter piece. Fast percussive sounds generate a disco like atmosphere.",
        ),
        (
            "electric guitar and drums",
            "A sour, bitter and salty piece. Really fast tempo. The guitar is distorted and plays in metal style.",
        ),
        ("drums and bass", "A salty and sour piece. Low and percussive sounds."),
        (
            "electric guitar and drums",
            "A salty and a little sour piece. Fast tempo with a guitar playing chords rythmically over the drums accompaniment.",
        ),
        (
            "electric guitar and drums",
            "A sour and little salty piece. Fast tempo with a guitar playing fast chords over the drums accompaniment.",
        ),
        (
            "electric guitar and drums",
            "A sour and salty piece. Fast tempo with a guitar playing rythmically chords over the fast drums accompaniment.",
        ),
        (
            "electronic",
            "A sour, salty and bitter piece. Fast tempo with a lot of electronic rythmic sounds.",
        ),
        (
            "electronic",
            "A sour and bitter piece. Slow tempo. Low and dissonant background sounds.",
        ),
        (
            "electronic",
            "A bitter, sour and salty piece. A high arpeggio in the background accompains a low guitar melody.",
        ),
        ("piano", "A sweet piece. A simple melody is being played over some chords."),
        ("piano", "A sweet piece. A piano plays continuously a simple arpeggio."),
        (
            "electronic",
            "A sweet and salty piece. Fast and short sounds are played over a low and stable musical carpet.",
        ),
        ("bells", "A bitter and a little sour piece. Bells play a low melody."),
        (
            "piano and strings",
            "A sweet and peaceful piece. The piano plays a simple melody over a continuous and fast accompaniment by the strings.",
        ),
        ("piano", "A sweet piece. The piano plays a simple and very high melody."),
        ("piano", "A sweet piece. The piano plays an high and continuous melody."),
        (
            "electronic",
            "A sweet piece. The instruments sound like plucked strings. A high percussive accompaniment in the background is covered by a simple melody.",
        ),
        (
            "electronic",
            "A sweet piece. A nice and simple arpeggio is the background for really high and soft sounds.",
        ),
        (
            "marimba",
            "A sweet, sour, salty and bitter piece. Percussive sounds generate a rythmic melody.",
        ),
        (
            "marimba",
            "A sweet and rythmic piece. The marimba plays a continuous and engaging melody.",
        ),
        (
            "piano",
            "A sweet and salty piece. The piano plays a jazzy melody over a low and nice arpeggio.",
        ),
        (
            "electronic",
            "A sweet and little salty piece. High percussive sounds are played over a nice middle-low accompaniment.",
        ),
        (
            "piano and strings",
            "A sweet piece. The piano plays a rythmic melody over a continuous and high note by the strings.",
        ),
        (
            "electronic",
            "A sweet and rythmic piece. Fast and soft high notes are played frenetically over a low and pacific background.",
        ),
        ("electronic", "A mostly salty piece. Slow tempo, with no melody."),
        (
            "piano",
            "A sweet and little bitter piece. The piano plays a high melody over a continuous arpeggio.",
        ),
        (
            "guitar",
            "A sweet piece. The guitar plays a really delicate and touching arpeggio.",
        ),
        (
            "electronic",
            "A sweet piece. A high melody that sounds like a flute is played over an arpeggio and long harmonies in the background.",
        ),
        # 68/69 ?
        (),
    ]


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
        with (dst / f"{song.stem}.json").open("w") as f:
            json.dump(asdict(Metadata.from_file(song)), f, indent=4)


if __name__ == "__main__":
    main()
