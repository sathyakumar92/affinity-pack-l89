import winreg
import subprocess
import ctypes
from typing import Optional, List

def get_registry_value(key: str, value: str) -> Optional[str]:
    """
    Retrieve a value from the Windows registry.

    Args:
        key (str): The registry key path.
        value (str): The name of the value to retrieve.

    Returns:
        Optional[str]: The value as a string if found, otherwise None.
    """
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key) as registry_key:
            return winreg.QueryValueEx(registry_key, value)[0]
    except FileNotFoundError:
        print(f"Registry key not found: {key}")
        return None
    except Exception as e:
        print(f"Error accessing registry: {e}")
        return None

def list_running_processes() -> List[str]:
    """
    List all currently running processes on the system.

    Returns:
        List[str]: A list of names of running processes.
    """
    try:
        process_list = subprocess.check_output(['tasklist'], universal_newlines=True)
        processes = []
        for line in process_list.splitlines()[3:]:
            parts = line.split()
            if parts:
                processes.append(parts[0])
        return processes
    except Exception as e:
        print(f"Error listing processes: {e}")
        return []

def kill_process(name: str) -> bool:
    """
    Kill a running process by name.

    Args:
        name (str): The name of the process to kill.

    Returns:
        bool: True if the process was successfully killed, False otherwise.
    """
    try:
        subprocess.run(['taskkill', '/F', '/IM', name], check=True)
        return True
    except subprocess.CalledProcessError:
        print(f"Failed to kill process: {name}")
        return False
    except Exception as e:
        print(f"Error killing process: {e}")
        return False

def is_admin() -> bool:
    """
    Check if the current user has administrative privileges.

    Returns:
        bool: True if the user is an administrator, False otherwise.
    """
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception as e:
        print(f"Error checking admin status: {e}")
        return False

def run_as_admin(cmd: str) -> int:
    """
    Run a command with administrative privileges.

    Args:
        cmd (str): The command to run.

    Returns:
        int: The exit code of the command.
    """
    try:
        result = subprocess.run(['runas', '/user:Administrator', cmd], check=True)
        return result.returncode
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {e}")
        return e.returncode
    except Exception as e:
        print(f"Error running command as admin: {e}")
        return -1
