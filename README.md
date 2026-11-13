# Social Media OCR Pipeline

This pipeline extracts texts from images (i.e., screenshots) of social media posts using PaddleOCR (PP-OCRv5). 

The defined input file is a folder of images (in .jpeg, .jpg, or .png form) and outputs a .csv with one full row per image. Each row includes the extracted text, an average confidence score, and a flag for low-confidence reads. Note: If the use-case requires comments to be separated from the original post, the aggregation step should be disabled (i.e., the groupby block in OCR_script.py)


## Installation

Tested with Python 3.12.

The requirements.txt file contains the necessary packages for this script: PaddleOCR, paddlepaddle, and pandas.

```
pip install -r requirements.txt
```

Note: The first run downloads and initates the PaddleOCR models, so it may take a few minutes.


## Usage

```
python3 OCR_script.py --input example_data/ --output results.csv
```

- `--input` (required): folder containing `.png`, `.jpg`, or `.jpeg` screenshots
- `--output` (optional): path for the output CSV (default: `ocr_results.csv`)


## Output

One row per image, with these columns:

- `image`: file name

- `text`: All recognized lines joined with spaces, in the order the model read them. The returned text is not cleaned, meaning that all raw text including emojis, punctuations, urls, or usernames are retained. 

- `confidence`: The confidence score is calculated by PaddleOCR. These are averaged across all lines of text recognized in an image, and ranges from 0 to 1. Note: In our testing and original study, confidence scores have a tendency to skew high. For this reason, 90% was used as the threshold below.

- `low_confidence`: Posts with an averaged confidence score of less than 90% are flagged. This flag uses Boolean logic, such that TRUE indicates a low confidence post extraction. To change the cutoff, edit the threshold in `OCR_script.py`.


## Known limitations

- Text may be misread by the model. For instance, one of the example posts 'text' produced a garbled output. This is caught by the low confidence flag, which should prompt manual review. 
- Confidence scores are calculated by PaddleOCR, as a measure of how sure the model is -- it does not indicate whether the text recognition was correct.
- While the low confidence flag can help to identify misread posts, it is incumbent upon the user to conduct more thorough reviews of the models performance as necessary. 
- In extraction, lines are joined in the model's read order, which may or may not match the visual order on complex layouts. 



## Data and ethics

The posts used in the original study can't be shared due to data sensitivity. The files in `example_data/` are posts from public or commercial social media platforms for this repository. All usernames have been anonymized. 

This project has been developed for research purposes only. Users are responsible for complying with the terms of service of any platform they collect screenshots from and within relevant research ethics requirements.



## Citation and license

This tool uses [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) (Apache 2.0). 

```bibtex
@misc{cui2025paddleocr30technicalreport,
      title={PaddleOCR 3.0 Technical Report},
      author={Cheng Cui and Ting Sun and Manhui Lin and Tingquan Gao and Yubo Zhang and Jiaxuan Liu and Xueqing Wang and Zelun Zhang and Changda Zhou and Hongen Liu and Yue Zhang and Wenyu Lv and Kui Huang and Yichao Zhang and Jing Zhang and Jun Zhang and Yi Liu and Dianhai Yu and Yanjun Ma},
      year={2025},
      eprint={2507.05595},
      archivePrefix={arXiv},
      primaryClass={cs.CV},
      url={https://arxiv.org/abs/2507.05595}}
 ```

If you use this script, please cite: 

DaVisio, K. (2026). *Social Media OCR Pipeline* [Analytic Script]. GitHub. https://github.com/kdavisio/Social-Media-OCR-Pipeline

You may also see [`CITATION.cff`](CITATION.cff).

Licensed under MIT. See `LICENSE`.
