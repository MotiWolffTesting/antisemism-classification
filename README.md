# Antisemitism Classification Data Analysis

A Python project for analyzing and classifying tweets related to antisemitism. This tool processes Twitter data, cleans text content, and generates comprehensive analysis reports.

## Overview

This project takes a dataset of tweets and performs analysis to understand patterns in antisemitic content. It includes data cleaning, text preprocessing, and statistical analysis to identify trends and characteristics in the dataset.

## Features

- **Data Analysis**: Analyzes tweet distribution, word counts, and text characteristics
- **Text Cleaning**: Removes punctuation, converts to lowercase, and filters relevant content
- **Statistical Reporting**: Generates detailed reports with analysis results
- **Data Export**: Saves cleaned datasets and analysis results

## Project Structure
antisemism-classification/
├── data/
│ └── tweets_dataset.csv # Input dataset
├── src/
│ ├── main.py # Main execution script
│ ├── data_analyzer.py # Core analysis functionality
│ ├── data_loader.py # Data loading utilities
│ ├── text_cleaner.py # Text preprocessing
│ ├── report_builder.py # Report generation
│ ├── report_displayer.py # Report display utilities
│ └── report_manager.py # Report management
└── results/
├── results.json # Analysis results
└── tweets_dataset_cleaned.csv # Cleaned dataset

## Usage

1. Ensure your dataset is in the `data/` directory as `tweets_dataset.csv`
2. Run the main analysis script:

```bash
cd src
python main.py
```

The script will:
- Load and analyze the original dataset
- Clean and preprocess the text data
- Generate analysis reports
- Save results to the `results/` directory

## Data Format

The input dataset should contain:
- `Text`: The tweet content
- `Biased`: Classification label (0 for non-antisemitic, 1 for antisemitic)

## Output

The analysis produces:
- **Cleaned Dataset**: Preprocessed tweets saved as CSV
- **Analysis Report**: JSON file containing statistical analysis results
- **Console Output**: Progress updates and summary statistics

## Requirements

- Python 3.x
- pandas
- Standard Python libraries (re, collections, typing)

## Analysis Features

- Tweet distribution analysis by classification
- Average word count per category
- Longest tweets identification
- Common word frequency analysis
- Text cleaning statistics