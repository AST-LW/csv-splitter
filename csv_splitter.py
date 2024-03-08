import os
import math
import pandas as pd
import glob

from filesys_operations import FilesysOperations


class CSVUtils:
    def __init__(self):
        self.csv_file_path = None
        self.workspace_directory_split = os.path.join(
            os.path.abspath(""), "workspace", "split")
        self.workspace_directory_downloads = os.path.join(
            os.path.abspath(""), "workspace", "downloads")
        self.workspace_directory_merge = os.path.join(
            os.path.abspath(""), "workspace", "merge")
        self.data_frame = None

    def _read_csv(self):
        self.data_frame = pd.read_csv(self.csv_file_path)

    def get_number_of_rows(self):
        return self.data_frame.shape[0]

    def get_file_size(self, unit: int = "mb"):
        number_of_bytes: int = os.path.getsize(self.csv_file_path)
        if unit == "mb":
            return round(number_of_bytes / (1000 * 1000), 1)

    # Main logic for CSV split
    def split_csv(self, csv_filepath: str, threshold_file_size: int):
        try:
            self.csv_file_path = csv_filepath
            self._read_csv()
            # Step - 1: Check the size of the CSV file, if it's within the threshold then return
            if self.get_file_size() <= threshold_file_size:
                return True

            # Step - 2: Number of csv file split required
            number_csv_file_split: int = math.ceil((
                self.get_file_size() / threshold_file_size))

            # Step - 3: Distribution of records among the split files
            total_number_of_rows = self.get_number_of_rows()
            number_of_rows_in_each_splitted_csv_file = math.ceil(
                total_number_of_rows / number_csv_file_split)

            [start_index, end_index] = [
                0, number_of_rows_in_each_splitted_csv_file]

            for i in range(number_csv_file_split):

                # Create the workspace directory for storing the splitted CSV files
                FilesysOperations.create_dirs(self.workspace_directory_split)

                # Step - 4: Storing the records with naming convention of - *_split_<index>.csv
                self.data_frame.iloc[start_index:end_index, :].to_csv(
                    f"{self.workspace_directory_split}/{os.path.basename(self.csv_file_path).split('.')[0]}_split_{i+1}.csv", index=False)
                start_index = end_index
                end_index += number_of_rows_in_each_splitted_csv_file
                if end_index > total_number_of_rows:
                    end_index = total_number_of_rows + 1  # include the last row as well

        except Exception as e:
            print(f"Encountered error while splitting the CSV files")

    def merge_csv(self, folder_name: str):
        file_pattern = f"{folder_name}_split_*.csv"
        csv_path_pattern = os.path.join(
            self.workspace_directory_downloads, file_pattern)
        matched_csv_files: list[str] = glob.glob(csv_path_pattern)
        matched_csv_files.sort()

        data_frames = []
        merged_data_frame = None

        for csv_file in matched_csv_files:
            data_frames.append(pd.read_csv(csv_file))

            merged_data_frame = pd.concat(data_frames)

        FilesysOperations.create_dirs(self.workspace_directory_merge)

        merged_data_frame.to_csv(
            f"{self.workspace_directory_merge}/{folder_name}_merged.csv", index=False)
