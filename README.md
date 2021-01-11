# mcs-cycic-analysis

Library and scripts to analyze CycIC entangled datasets for the Machine Common Sense (MCS) program.

# One-time setup

## Create the Python virtual environment

From the current directory:

    python3 -m venv venv

## Activate the virtual environment

On Unix:

    source venv/bin/activate

On Windows

    venv\Scripts\activate

## Install the dependencies

    pip install -r requirements.txt

## Download the CycIC 3 sample dataset

Download and expand the CycIC entangled sample dataset (12/1) to `data/downloaded/cycic3_sample`.

The sample dataset should consist of:

* `cycic3_question_links.csv`
* `cycic3a_sample_labels.jsonl`
* `cycic3a_sample_questions.jsonl`
* `cycic3b_sample_labels.jsonl`
* `cycic3b_sample_questions.jsonl`


# Running tests

Activate the virtual environment as above, then run:

    pytest

# Creating spreadsheets (CSV files)

1. Activate the virtual environment as above
1. Run the command: `python3 -m mcs_cycic_analysis create-spreadsheets`

The spreadsheet CSV files will be written to `data/spreadsheets/cycic3_sample`. This directory will be created if necessary.

The files are intended to be different sheets/tabs in a Google Sheet or Excel file.

# Development

The `mcs-cycic-analysis` code base consists of:
* a library of models for capturing the CycIC dataset
* a command line interface for reading, writing, and manipulating models

Start by looking at `mcs_cycic_analysis.cli.commands.create_spreadsheet_command` as an entry point.
