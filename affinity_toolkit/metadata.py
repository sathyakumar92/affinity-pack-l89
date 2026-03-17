from pathlib import Path
import json
from dataclasses import dataclass
from typing import Any, Dict, Optional

@dataclass
class Metadata:
    title: Optional[str] = None
    author: Optional[str] = None
    created: Optional[str] = None
    modified: Optional[str] = None
    description: Optional[str] = None

class AffinityDesignerMetadataReader:
    @staticmethod
    def read(path: Path) -> Metadata:
        """
        Reads metadata from a JSON file at the specified path.

        Args:
            path (Path): The path to the metadata file.

        Returns:
            Metadata: An instance of Metadata containing the extracted data.

        Raises:
            FileNotFoundError: If the specified file does not exist.
            json.JSONDecodeError: If the file is not a valid JSON.
        """
        if not path.is_file():
            raise FileNotFoundError(f"Metadata file not found: {path}")

        with path.open('r', encoding='utf-8') as file:
            try:
                data: Dict[str, Any] = json.load(file)
                return Metadata(
                    title=data.get('title'),
                    author=data.get('author'),
                    created=data.get('created'),
                    modified=data.get('modified'),
                    description=data.get('description')
                )
            except json.JSONDecodeError as e:
                raise json.JSONDecodeError(f"Error decoding JSON from {path}: {e}")

    @staticmethod
    def write(path: Path, metadata: Metadata) -> bool:
        """
        Writes metadata to a JSON file at the specified path.

        Args:
            path (Path): The path where the metadata file should be saved.
            metadata (Metadata): The Metadata instance to write to the file.

        Returns:
            bool: True if the write operation was successful, False otherwise.
        """
        try:
            with path.open('w', encoding='utf-8') as file:
                json.dump(metadata.__dict__, file, ensure_ascii=False, indent=4)
            return True
        except IOError as e:
            print(f"Error writing to file {path}: {e}")
            return False
