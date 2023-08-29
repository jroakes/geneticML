import os
import json
import glob
import shutil

from utils.constants import DYNAMIC_FOLDER, DYNAMIC_MAIN

def read_file(file_path: str) -> str:
    """
    Read the contents of a file and return it as a string.
    """
    with open(file_path, 'r') as f:
        return f.read()


def write_file(file_path: str, content: str) -> None:
    """
    Write the given string into a file.
    """
    with open(file_path, 'w') as f:
        f.write(content)


def list_files(directory_path: str) -> list:
    """
    List all files in a directory.
    """
    return glob.glob(f"{directory_path}/*")


def make_directory(directory_path: str) -> None:
    """
    Create a directory if it doesn't exist.
    """
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)


def delete_directory(directory_path: str) -> None:
    """
    Delete a directory if it exists.
    """
    if os.path.exists(directory_path):
        shutil.rmtree(directory_path)


def delete_file(file_path: str) -> None:
    """
    Delete a file if it exists.
    """
    if os.path.exists(file_path):
        os.remove(file_path)


def read_config():
    """
    Read the config.json file and return its contents as a Python dictionary.
    """
    try: 
        with open('config.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        create_config()
        return read_config()
    
    except json.decoder.JSONDecodeError:
        create_config()
        return read_config()
    
    else:
        raise Exception("Unknown error occurred while reading config.json")




def write_config(data):
    """
    Write a Python dictionary into the config.json file overwriting its contents.
    """
    with open('config.json', 'w') as f:
        json.dump(data, f, indent=4, sort_keys=True)


def create_config():
    """
    Create a config.json file with the default values.
    """
    data = {
        'last_known_objective': '',
        'last_known_expected_result': '',
        'code_files': [],
        'change_log': [],
        'run_log': []
    }
    write_config(data)


def maybe_create_prompt_log():
    """
    Create a prompt.log file if it doesn't exist.
    """
    if not os.path.exists('prompt.log'):
        write_file('prompt.log', '')


def update_prompt_log(prompt: str):
    """
    Append the given prompt to the prompt.log file.
    """
    maybe_create_prompt_log()
    
    with open('prompt.log', 'a') as f:
        f.write(prompt + '\n')



