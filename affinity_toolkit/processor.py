import json
from pathlib import Path
from typing import Dict, Any, List, Callable, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

class AffinityDesignerProcessor:
    def __init__(self, client: 'AffinityDesignerClient'):
        """
        Initialize the AffinityDesignerProcessor with the provided client.

        :param client: An instance of AffinityDesignerClient.
        """
        self.client = client

    def process_file(self, path: Path, progress_callback: Optional[Callable[[str], None]] = None) -> Dict[str, Any]:
        """
        Process a single Affinity Designer file.

        :param path: The file path to process.
        :param progress_callback: Optional callback to report progress.
        :return: A dictionary containing extracted data.
        """
        if not path.exists() or not path.is_file():
            logging.error(f"File not found: {path}")
            raise FileNotFoundError(f"The file {path} does not exist.")

        try:
            if progress_callback:
                progress_callback(f"Processing file: {path.name}")

            data = {
                "text": self.extract_text(path),
                "metadata": self.extract_metadata(path)
            }

            if progress_callback:
                progress_callback(f"Finished processing file: {path.name}")

            return data

        except Exception as e:
            logging.error(f"Error processing file {path}: {e}")
            raise

    def extract_text(self, path: Path) -> str:
        """
        Extract text content from the Affinity Designer file.

        :param path: The file path to extract text from.
        :return: A string containing the extracted text.
        """
        try:
            with open(path, 'r') as file:
                content = json.load(file)
                text_elements = content.get('textElements', [])
                extracted_text = ' '.join(element.get('content', '') for element in text_elements)
                return extracted_text

        except json.JSONDecodeError as e:
            logging.error(f"Failed to decode JSON from {path}: {e}")
            raise
        except Exception as e:
            logging.error(f"Error extracting text from {path}: {e}")
            raise

    def extract_metadata(self, path: Path) -> Dict:
        """
        Extract metadata from the Affinity Designer file.

        :param path: The file path to extract metadata from.
        :return: A dictionary containing the extracted metadata.
        """
        try:
            with open(path, 'r') as file:
                content = json.load(file)
                metadata = {
                    "author": content.get('author', 'Unknown'),
                    "created": content.get('created', 'Unknown'),
                    "modified": content.get('modified', 'Unknown'),
                }
                return metadata

        except json.JSONDecodeError as e:
            logging.error(f"Failed to decode JSON from {path}: {e}")
            raise
        except Exception as e:
            logging.error(f"Error extracting metadata from {path}: {e}")
            raise

    def batch_process(self, paths: List[Path], progress_callback: Optional[Callable[[str], None]] = None) -> List[Dict]:
        """
        Process multiple Affinity Designer files in batch.

        :param paths: A list of file paths to process.
        :param progress_callback: Optional callback to report progress.
        :return: A list of dictionaries containing extracted data from each file.
        """
        results = []
        for path in paths:
            try:
                result = self.process_file(path, progress_callback)
                results.append(result)
            except Exception as e:
                logging.error(f"Failed to process file {path}: {e}")

        return results
