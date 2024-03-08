import os
import glob


class FilesysOperations:

    @staticmethod
    def create_dirs(path: str):
        try:
            if not os.path.isdir(path):
                os.makedirs(path)
        except:
            print(f"Error in creating recursive directories.")

    def matched_files(pattern: str):
        matched_file_paths = glob.glob(pattern)
        matched_file_paths.sort()
        return matched_file_paths
