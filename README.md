# CSV Cleaner

## Overview
A small Python command-line tool that cleans CSV files. It trims leading and trailing whitespace from cell values, removes duplicate rows, and saves cleaned data to a new CSV file. It also includes basic input validation and safeguards to help prevent accidental overwriting of existing files.

## Features
- Trims leading and trailing whitespace from cell values
- Removes duplicate rows while preserving the first occurrence
- Allows users to specify if the CSV contains a header
- Prevents the input and output paths from being the same
- Requests confirmation before overwriting existing files

## Requirements
- Python version 3.14
- No external packages needed; program runs using Python's standard library

## Installation
1. Clone this repository:
   ```bash 
   git clone https://github.com/camerongmc1/csv-cleaner.git
   ```
2. Navigate to the project repository:
   ```bash
   cd csv-cleaner
   ```
3. Ensure Python 3.14 is installed.

## Usage
Run the program from the project directory:
   ```bash
   python3.14 main.py
   ```
Follow the prompts to clean a CSV file:
    1. Enter the path to the input CSV file.
    2. Specify whether the CSV file contains a header row (`y` or `n`).
    3. Enter the desired output filename or path.
    4. If the output file already exists, choose whether to overwrite it.
    5. Review the summary displayed when cleaning is complete.

## Running Tests
The project includes a test suite built using Python's built-in `unittest` framework. The tests cover CSV reading and writing, whitespace trimming, duplicate removal, and input validation.

To run the full test suite, execute the following command from the project directory:

   ```bash
   python3.14 -B -m unittest -v
   ```

## Limitations
- Supports UTF-8 encoded CSV files only.
- Provides basic cleaning by trimming leading and trailing whitespace and removing duplicate rows.
- Does not validate data types, correct malformed data, or perform advanced data cleaning.
- Runs through a command-line interface; no graphical user interface is provided.