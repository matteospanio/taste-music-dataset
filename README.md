# taste-music-dataset

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![DOI](https://zenodo.org/badge/801652017.svg)](https://doi.org/10.5281/zenodo.14879128)

This is the repository to make a fine-tuning dataset for [MusicGEN](https://github.com/facebookresearch/audiocraft/blob/main/docs/MUSICGEN.md), a model for music generation by Facebook Research.

This dataset has been released under the project [A Multimodal Symphony: Integrating Taste and Sound through Generative AI](https://osf.io/xs5jy/), and is an attachment to the paper *A Multimodal Symphony: Integrating Taste and Sound through Generative AI by Matteo Spanio, Massimiliano Zampini, Antonio Rodà and Franco Pierucci*.

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

## Citation

If you use this code or the data in your research, please cite the following article:

```
@misc{spanio2025multimodalsymphonyintegratingtaste,
      title={A Multimodal Symphony: Integrating Taste and Sound through Generative AI}, 
      author={Matteo Spanio and Massimiliano Zampini and Antonio Rodà and Franco Pierucci},
      year={2025},
      eprint={2503.02823},
      archivePrefix={arXiv},
      primaryClass={cs.SD},
      url={https://arxiv.org/abs/2503.02823}, 
}
```

## Acknowledgements

We thank the authors of the [Taste & Affect Music Database](https://osf.io/2cqa5/)[^1], a set of 100 musical stimuli suitable for crossmodal and affective research, on which this dataset is based.

## License

This dataset is distributed under the [CC BY 4.0](LICENSE) license.

[^1]: Guedes, D., Prada, M., Garrido, M. V., & Lamy, E. (2022, November 24). The Taste & Affect Music Database. Retrieved from osf.io/2cqa5
