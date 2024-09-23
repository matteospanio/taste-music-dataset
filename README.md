# taste-music-dataset

This is the repository to make a fine-tuning dataset for MusicGEN.

> Under construction

## How to use

1. Clone this repository
2. Run `make data` to download the dataset and generate the fine-tuning dataset

At the end of the process you should have a folder named `data` with the following structure:
```
data
├── dataset
├── eval
├── metadata_1.xlsx
├── metadata_2.xlsx
└── train
```

Move to your MusicGEN folder and copy the dataset to make some finetuning, if you cloned the audiocraft repo you can run the following commands from the audiocraft folder:

```bash
mv /path/to/taste-music-dataset/data/dataset ./dataset/finetune
mv /path/to/taste-music-dataset/data/train ./egs/train
mv /path/to/taste-music-dataset/data/eval ./egs/eval
```

## License

[GPL-3.0](LICENSE)
