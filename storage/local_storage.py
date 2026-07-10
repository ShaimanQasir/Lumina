import os
import shutil
from typing import Optional
from config.config import Config

class LocalStorage:
    def __init__(self, config: type[Config] = Config):
        self.raw_dir = config.LOCAL_RAW_DIR
        self.processed_dir = config.LOCAL_PROCESSED_DIR
        self._create_directories()

    def _create_directories(self) -> None:
        """
        Create raw and processed directories if they don't exist
        """
        os.makedirs(self.raw_dir, exist_ok=True)
        os.makedirs(self.processed_dir, exist_ok=True)

    def upload_file(self, content: str, file_name: str, metadata: dict) -> None:
        """
        Save a file locally with metadata written as header or just ignoring metadata 
        for simplicity, we'll just save the content.
        parameters:
            content: Content of the file to be saved
            file_name: Name of the file
        """
        file_path = os.path.join(self.raw_dir, file_name)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            # We can optionally write metadata at the top of the file
            f.write(content)

    def list_files(self, directory: Optional[str] = None) -> list:
        """
        return: List of all files in the given directory
        parameters:
            directory: Directory to list files from. Defaults to raw_dir.
        """
        target_dir = directory or self.raw_dir
        file_list = []
        for root, _, files in os.walk(target_dir):
            for file in files:
                # get relative path
                rel_dir = os.path.relpath(root, target_dir)
                if rel_dir == ".":
                    file_list.append(file)
                else:
                    file_list.append(os.path.join(rel_dir, file))
        return file_list

    def copy_file(self, source_file_path: str) -> None:
        """
        Copy files from the raw directory to processed directory
        parameters:
            source_file_path: Relative path of the file to be copied
        """
        src_path = os.path.join(self.raw_dir, source_file_path)
        dest_path = os.path.join(self.processed_dir, source_file_path)
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        shutil.copy2(src_path, dest_path)

    def delete_file(self, key: str) -> None:
        """
        Delete a file from the raw directory
        parameters:
            key: Relative path of the file to be deleted
        """
        src_path = os.path.join(self.raw_dir, key)
        if os.path.exists(src_path):
            os.remove(src_path)

    def move_files(self, source_file_path: str):
        """
        Move a file within the raw directory to the processed directory
        parameters:
            source_file_path: Relative path of the file to be moved
        """
        self.copy_file(source_file_path)
        self.delete_file(source_file_path)

    def read_object(self, source_file_path: str) -> str:
        """
        Read a file from the raw directory
        parameters:
            source_file_path: Relative path of the file to be read
        """
        src_path = os.path.join(self.raw_dir, source_file_path)
        with open(src_path, "r", encoding="utf-8") as f:
            return f.read()
