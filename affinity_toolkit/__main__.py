import argparse
import json
import os
import csv
from pathlib import Path
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class AffinityFile:
    name: str
    path: Path
    size: int

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "path": str(self.path),
            "size": self.size,
        }

def scan_directory(directory: str) -> List[AffinityFile]:
    """Scan the specified directory for Affinity Designer files."""
    affinity_files = []
    try:
        for entry in os.listdir(directory):
            if entry.endswith(('.afdesign', '.afpub')):
                file_path = Path(directory) / entry
                affinity_files.append(AffinityFile(name=entry, path=file_path, size=file_path.stat().st_size))
        print(f"Found {len(affinity_files)} Affinity files in '{directory}'.")
    except Exception as e:
        print(f"Error scanning directory: {e}")
    return affinity_files

def show_file_info(file_path: str) -> None:
    """Display information about a specific Affinity file."""
    try:
        path = Path(file_path)
        if not path.exists():
            print(f"File '{file_path}' does not exist.")
            return

        file_info = AffinityFile(name=path.name, path=path, size=path.stat().st_size)
        print(json.dumps(file_info.to_dict(), indent=4))
    except Exception as e:
        print(f"Error retrieving file info: {e}")

def export_data(files: List[AffinityFile], format: str) -> None:
    """Export file data to JSON or CSV format."""
    try:
        if format == 'json':
            with open('affinity_files.json', 'w') as json_file:
                json.dump([file.to_dict() for file in files], json_file, indent=4)
            print("Data exported to 'affinity_files.json'.")
        elif format == 'csv':
            with open('affinity_files.csv', 'w', newline='') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=AffinityFile.__dataclass_fields__.keys())
                writer.writeheader()
                for file in files:
                    writer.writerow(file.to_dict())
            print("Data exported to 'affinity_files.csv'.")
        else:
            print("Unsupported format. Please choose 'json' or 'csv'.")
    except Exception as e:
        print(f"Error exporting data: {e}")

def batch_process(files: List[AffinityFile]) -> None:
    """Perform batch processing on multiple Affinity files."""
    for file in files:
        print(f"Processing file: {file.name} at {file.path}...")
        # Placeholder for actual processing logic
        # Add your processing code here
    print("Batch processing completed.")

def main() -> None:
    parser = argparse.ArgumentParser(description="Affinity Designer Toolkit for Windows")
    subparsers = parser.add_subparsers(dest='command')

    # Scan command
    scan_parser = subparsers.add_parser('scan', help="Scan directory for Affinity Designer files")
    scan_parser.add_argument('directory', type=str, help="Directory to scan")

    # Info command
    info_parser = subparsers.add_parser('info', help="Show information about a specific file")
    info_parser.add_argument('file', type=str, help="Path to the Affinity file")

    # Export command
    export_parser = subparsers.add_parser('export', help="Export data to JSON or CSV")
    export_parser.add_argument('format', choices=['json', 'csv'], help="Format to export data")

    # Batch command
    batch_parser = subparsers.add_parser('batch', help="Batch process multiple files")
    batch_parser.add_argument('files', nargs='+', type=str, help="List of Affinity files to process")

    args = parser.parse_args()

    if args.command == 'scan':
        scan_directory(args.directory)
    elif args.command == 'info':
        show_file_info(args.file)
    elif args.command == 'export':
        files = scan_directory(Path().resolve())  # Scanning current directory for demo
        export_data(files, args.format)
    elif args.command == 'batch':
        files = [AffinityFile(name=Path(file).name, path=Path(file), size=Path(file).stat().st_size) for file in args.files]
        batch_process(files)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
