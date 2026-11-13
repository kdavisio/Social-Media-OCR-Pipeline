#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Social Media OCR Pipeline 
Kaitlyn DaVisio 
Goal: Develop a pipeline to extract text from image-based posts using Optical Character Recognition (OCR)

Last updated: October 2026
"""

# Loading necessary packages 
import os
import pandas as pd
import argparse

parser = argparse.ArgumentParser(description="Extracts text from social media screenshots using PaddleOCRv5.")
parser.add_argument("--input", required=True, help="Name of the folder containing .png/.jpg/.jpeg screenshots")
parser.add_argument("--output", default="ocr_results.csv", help="Filepath and name for the output CSV")
args = parser.parse_args()


##Model set-up 

# Initialize PaddleOCR 
from paddleocr import PaddleOCR

ocr = PaddleOCR(
    ocr_version="PP-OCRv5",
    use_doc_orientation_classify=False, # Controls document orientation classifer (True/False)
    use_doc_unwarping=True, #Controls text image rectification model (True/False)
    use_textline_orientation=True)  #Controls text line orientation classification model (True/False)
#Unwarping and Line Orientation helps to correctly identify different lines/sections of text


#Define input and output locations
image_files = [os.path.join(args.input, f) for f in os.listdir(args.input) 
               if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
all_results = []


##Applying OCR model to data 

#runs loop over each .png, .jpg., or .jpeg file in folder  
print("Running...")
for img_path in image_files:
    result = ocr.predict(img_path) 
    for res in result:
        for text, score in zip(res['rec_texts'], res['rec_scores']):
            all_results.append({
                'image': os.path.basename(img_path),
                'text': text,
                'confidence': score
            })
print("Done!")

df = pd.DataFrame(all_results)


##Natively, each 'translated' line of the image comes over as one line in the .csv
## We concatenate by the file name and average assigned confidence values

#Aggregating by image 
df_agg = (
    df
    .groupby("image", as_index=False)    #group_by
    .agg({
        "text": lambda x: " ".join(x),   #concatenate all text with a SPACE, alt options are " | " for comma, or "\n" for newline
        "confidence": "mean"             #takes the mean of all confidence values by image 
    }))

df_agg["low_confidence"] = df_agg["confidence"] < .90 #posts below 90% confidence are flagged for manual review 

#convert to csv
df_agg.to_csv(args.output, index=False)
print(f"Saved {len(df_agg)} observations to {args.output}")





