# CSV Splitter and Supabase Storage Handling

This documentation provides a comprehensive guide on how to handle large CSV files efficiently by splitting them into smaller parts, uploading to Supabase storage, and then merging them back into a single file. This process is particularly useful when dealing with file size limitations during uploads.

## Prerequisites

-   Python 3.x
-   Supabase account and project setup

## Installation

Before running the scripts, ensure you have the necessary Python libraries and virtual environment installed.

1.  Create virtual environment

    ```bash
    python3 -m venv venv
    ```

2.  Activate the virtual environment

    ```bash
    # The following command is for UNIX based systems, look for corresponding command if using Windows
    source ./venv/bin/activate
    ```

3.  Install the python libraries

    ```bash
    pip3 install -r requirements.txt
    ```

## Environment setup

Ensure you have set up your Supabase credentials in a `.env` file at the root of your project directory. The `.env` file should contain your Supabase URL and Key:

```
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
```

## Project Structure

```
csv-splitter/
│
├── workspace/
│   ├── split/            # Directory for storing split CSV files
│   ├── downloads/        # Directory for storing downloaded CSV files from Supabase
│   └── merge/            # Directory for storing the final merged CSV file
│
├── dummy_csv_file_creator.py   # Script to create a dummy CSV file
├── csv_splitter.py             # Utility class for splitting and merging CSV files
├── supabase_utils.py           # Utility class for uploading and downloading from Supabase
├── filesys_operations.py       # Utility class for file system operations
└── main.py                     # Main script to orchestrate the CSV handling process
```

## Workflow Description

### Flow 1: Split and Upload CSV File to Supabase

1. **Create a Dummy CSV File**:

    - Run `dummy_csv_file_creator.py` to generate a new CSV file named `dummy_data.csv`. This file is intentionally larger than 50MB to simulate the threshold limit for uploads.

2. **Split the CSV File**:

    - Use the `split_csv` method in `csv_splitter.py` to split `dummy_data.csv` into smaller parts. These parts will be stored in `workspace/split` directory. Each part is ensured to be less than the 50MB threshold.

3. **Upload Split Files to Supabase**:
    - With `upload` method`supabase_utils.py`, upload the split files from the `workspace/split` directory to your designated Supabase storage bucket.

### Flow 2: Download and Merge CSV Files from Supabase

1. **Download Split Files**:

    - Using `download` method in `supabase_utils.py`, download the split files from Supabase storage to the `workspace/downloads` directory.

2. **Merge CSV Files**:
    - Finally, merge the downloaded split files back into a single CSV file using the `merge_csv` method in `csv_splitter.py`. The merged file will be saved in the `workspace/merge` directory.

## Usage

To execute the entire process, run the `main.py` script:

```bash
python3 main.py
```

This script orchestrates the process by:

-   Creating a dummy CSV file that exceeds the upload size limit.
-   Splitting the large CSV file into smaller parts.
-   Uploading the parts to Supabase.
-   Downloading the parts from Supabase.
-   Merging the parts back into a single CSV file.
