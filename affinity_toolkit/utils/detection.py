import os
import subprocess
from pathlib import Path
from typing import Optional

def find_installation() -> Optional[Path]:
    """Find the installation path of Affinity Designer on Windows.

    This function checks common installation paths for Affinity Designer and returns
    the path if found.

    Returns:
        Optional[Path]: The installation path if found, otherwise None.
    """
    common_paths = [
        Path("C:/Program Files/Serif/Affinity Designer/Affinity Designer.exe"),
        Path("C:/Program Files (x86)/Serif/Affinity Designer/Affinity Designer.exe"),
        Path("C:/Program Files/Affinity/Designer/Affinity Designer.exe"),
        Path("C:/Program Files (x86)/Affinity/Designer/Affinity Designer.exe"),
    ]
    
    for path in common_paths:
        if path.exists():
            return path
    return None

def get_version() -> Optional[str]:
    """Get the version of Affinity Designer installed on the system.

    This function attempts to retrieve the version of Affinity Designer
    by executing the application with a version flag.

    Returns:
        Optional[str]: The version string if successfully retrieved, otherwise None.
    """
    executable_path = get_executable_path()
    if executable_path:
        try:
            result = subprocess.run([executable_path, '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.strip()
        except Exception as e:
            print(f"Error retrieving version: {e}")
    return None

def is_installed() -> bool:
    """Check if Affinity Designer is installed on the system.

    This function checks for the presence of the Affinity Designer executable.

    Returns:
        bool: True if installed, False otherwise.
    """
    return find_installation() is not None

def get_executable_path() -> Optional[Path]:
    """Get the executable path of Affinity Designer.

    This function returns the path of the Affinity Designer executable if it exists.

    Returns:
        Optional[Path]: The executable path if found, otherwise None.
    """
    installation_path = find_installation()
    if installation_path:
        return installation_path
    return None
