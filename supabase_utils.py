import os
from dotenv import find_dotenv, load_dotenv
from supabase import create_client

from filesys_operations import FilesysOperations

load_dotenv(find_dotenv())


class Supabase:
    def __init__(self, bucket_name):
        self._supabase_url = os.getenv("SUPABASE_URL")
        self._supabase_key = os.getenv('SUPABASE_KEY')
        self.workspace_directory_split = os.path.join(
            os.path.abspath(""), "workspace", "split")
        self.workspace_directory_downloads = os.path.join(
            os.path.abspath(""), "workspace", "downloads")
        self.workspace_directory_merge = os.path.join(
            os.path.abspath(""), "workspace", "merge")

        self.supabase_client = create_client(
            supabase_key=self._supabase_key, supabase_url=self._supabase_url)
        self._bucket_name = bucket_name

    def create_bucket(self):
        try:
            self.supabase_client.storage.create_bucket(self._bucket_name)
        except Exception as e:
            print(f"Error in creating the bucket")

    def upload(self, filename: str, file_options: dict = {"content-type": "text/csv"}):
        try:
            file_pattern = f"{filename}_split_*.csv"
            csv_path_pattern = os.path.join(
                self.workspace_directory_split, file_pattern)
            csv_split_files = FilesysOperations.matched_files(csv_path_pattern)

            self.create_bucket()

            print(csv_split_files)

            for file_path in csv_split_files:
                with open(file_path, "rb") as file:
                    supastorage_file_path = filename + \
                        "/" + os.path.basename(file_path)
                    self.supabase_client.storage.from_(
                        self._bucket_name).upload(file=file, path=supastorage_file_path, file_options=file_options)
            return True
        except Exception as e:
            print(f"Error in uploading the file into the bucket: {e}")
            return False

    def download(self, folder_name: str):
        try:
            buckets_info = self.supabase_client.storage.from_(
                self._bucket_name).list(folder_name)
            print(buckets_info)
            for file_info in buckets_info:
                filename = file_info["name"]
                supabase_downloaded_file = self.supabase_client.storage.from_(
                    self._bucket_name
                ).download(folder_name + "/" + filename)

                # create "downloads" folder within "workspace" directory
                FilesysOperations.create_dirs(
                    self.workspace_directory_downloads)

                # write into downloads directory
                with open(self.workspace_directory_downloads + "/" + filename, "+wb") as file:
                    file.write(supabase_downloaded_file)
            return True
        except Exception as e:
            print(f"Error in downloading the file from bucket: {e}")
            return False
