import argparse as ap
import pathlib as pl
import json
from sklearn.model_selection import train_test_split


def main():
    parser = ap.ArgumentParser()
    parser.add_argument(
        "input",
        type=pl.Path,
        help="The folder containing the json metadata.",
    )
    parser.add_argument("output", type=pl.Path, help="The jsonl file to write to.")
    args = parser.parse_args()
    input: pl.Path = args.input
    out_dir: pl.Path = args.output

    out_dir.mkdir(exist_ok=True)
    pl.Path(out_dir / "train").mkdir(exist_ok=True)
    pl.Path(out_dir / "eval").mkdir(exist_ok=True)

    train_file: pl.Path = out_dir / "train" / "data.jsonl"
    eval_file: pl.Path = out_dir / "eval" / "data.jsonl"

    data = list(input.glob("*.json"))

    train, eval = train_test_split(data, test_size=0.15, random_state=42)

    with train_file.open("w") as out:
        for j in train:
            with j.open() as f:
                data = json.load(f)
            data["path"] = "dataset/finetune/" + j.stem + data["file_extension"]

            out.write(json.dumps(data) + "\n")

    with eval_file.open("w") as out:
        for j in eval:
            with j.open() as f:
                data = json.load(f)
            data["path"] = "dataset/finetune/" + j.stem + data["file_extension"]

            out.write(json.dumps(data) + "\n")


if __name__ == "__main__":
    main()
