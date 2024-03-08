import os


from dummy_csv_file_creator import create_dummy_csv_file
from csv_splitter import CSVUtils
from supabase_utils import Supabase

if __name__ == "__main__":
    THRESHOLD_SIZE = 50

    create_dummy_csv_file()
    CSVUtils().split_csv(os.path.join(os.path.abspath(
        ""), "dummy_data.csv"), THRESHOLD_SIZE)

    Supabase("dummy_bucket").upload("dummy_data")

    # End of first process

    Supabase("dummy_bucket").download("dummy_data")
    CSVUtils().merge_csv("dummy_data")
