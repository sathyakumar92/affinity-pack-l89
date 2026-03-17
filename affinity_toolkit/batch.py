import concurrent.futures
from pathlib import Path
from typing import List, Callable, Optional
from dataclasses import dataclass
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

@dataclass
class Result:
    path: Path
    success: bool
    data: Optional[dict] = None
    error: Optional[str] = None

class BatchProcessor:
    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers

    def process_directory(self, path: Path, pattern: str = "*") -> List[Result]:
        """Process all files in the specified directory matching the pattern."""
        results = []
        try:
            files_to_process = list(path.glob(pattern))
            logging.info(f"Found {len(files_to_process)} files to process in {path}")
            results = self.process_files(files_to_process)
        except Exception as e:
            logging.error(f"Error processing directory {path}: {e}")
        return results

    def process_files(self, paths: List[Path], callback: Callable = None) -> List[Result]:
        """Process a list of files concurrently."""
        results = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_path = {executor.submit(self.process_file, path, callback): path for path in paths}
            for future in concurrent.futures.as_completed(future_to_path):
                path = future_to_path[future]
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    logging.error(f"Error processing file {path}: {e}")
                    results.append(Result(path=path, success=False, error=str(e)))
        return results

    def process_file(self, path: Path, callback: Optional[Callable] = None) -> Result:
        """Process a single file and return the result."""
        try:
            # Simulate file processing logic
            logging.info(f"Processing file: {path}")
            data = {'filename': path.name}  # Example data extraction
            if callback:
                callback(data)
            return Result(path=path, success=True, data=data)
        except Exception as e:
            logging.error(f"Failed to process file {path}: {e}")
            return Result(path=path, success=False, error=str(e))
