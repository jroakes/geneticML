import re
import subprocess
from loguru import logger
from typing import List, Set
from interaction_manager import ask_user_for_permission


def get_code_dependencies(code: str) -> Set[str]:
    """
    Scans the Python code for import statements and returns a set of dependencies.

    Parameters:
    code (str): Python code to scan for import statements.

    Returns:
    Set[str]: A set of unique dependencies.
    """
    # Regular expressions for matching import statements
    import_patterns = [
        r"^import (\w+)",
        r"^from (\w+) import",
    ]
    
    dependencies = set()
    
    for pattern in import_patterns:
        for match in re.findall(pattern, code):
            dependencies.add(match)
            
    return dependencies



def check_and_install_dependencies(dependencies: List[str]) -> None:
    """
    Checks whether the specified Python libraries are installed. If they are not,
    prompts the user for permission to install them.

    Parameters:
    dependencies (List[str]): List of library names to check for.

    Returns:
    None
    """
    
    # Loop through each dependency to check if it's installed
    for dependency in dependencies:
        try:
            # Attempt to import the library
            subprocess.run(['python', '-c', f'import {dependency}'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError:
            # If the import failed, ask the user if they want to install the dependency
            user_response = ask_user_for_permission(f"The {dependency} library is not installed. Would you like to install it? (y/n)")
            
            if user_response:
                # If the user agrees, install the package
                try:
                    subprocess.run(['pip', 'install', dependency], check=True)
                except subprocess.CalledProcessError:
                    logger.error(f"Failed to install {dependency}.")
            else:
                logger.warning(f"Skipping the installation of {dependency}.")
