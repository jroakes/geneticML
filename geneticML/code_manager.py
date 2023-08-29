import os
import json
import subprocess
from loguru import logger
from typing import Union, Tuple

from session_manager import (
    update_dynamic_files,
    read_session_config,
    get_session,
    get_last_run_log_entry,
    get_last_change_log_entry,
    update_run_log,
    update_change_log,
)
from taxonomyml_interface import get_code
from dependency_manager import check_and_install_dependencies, get_code_dependencies
from utils.file_operations import (
    read_file,
    write_file,
    make_directory,
    delete_directory,
    list_files,
    delete_file,
)

from utils.constants import DYNAMIC_FOLDER, DYNAMIC_MAIN
from utils.prompts import (
    OUTLINE_PROMPT,
    FILE_PROMPT,
    IMPROVE_PROMPT,
    CREATE_PROMPT,
    build_action_selection_prompt,
)


def ensure_dynamic_directory() -> None:
    """
    Ensure that the directory exists. If not, create it.
    """
    make_directory(DYNAMIC_FOLDER)


def delete_dynamic_directory() -> None:
    """
    Delete the dynamic directory if it exists.
    """
    delete_directory(DYNAMIC_FOLDER)


def create_outline_and_files(objective: str) -> None:
    """
    Asks the language model to outline the files required for the objective
    and then iterates to populate each file.
    """

    # Generate a prompt to ask the language model for the necessary files and functionalities
    prompt = OUTLINE_PROMPT.format(objective=objective, DYNAMIC_MAIN=DYNAMIC_MAIN)

    # Get the outline response from the language model
    outline_response = get_code(prompt, response_type="json")

    try:
        # Safely parse the response into a Python dictionary
        code_outline = json.loads(outline_response)
    except json.JSONDecodeError:
        logger.error(
            "Received an invalid JSON response for the outline. Cannot proceed."
        )
        return

    # Initialize an empty dictionary to hold the filenames and their corresponding code
    code_files = {}

    for filename, functionality in code_outline.items():
        # Generate a prompt to ask the language model to generate code for each file
        prompt = FILE_PROMPT.format(filename=filename, functionality=functionality)

        # Get the code from the language model
        code_response = get_code(prompt, response_type="json")

        try:
            # Safely parse the response to get the generated code
            generated_code = json.loads(code_response)["code"]
        except (json.JSONDecodeError, KeyError):
            logger.error(
                f"Received an invalid JSON response for the file {filename}. Skipping."
            )
            continue

        dependencies = get_code_dependencies(generated_code)

        if dependencies:
            check_and_install_dependencies(dependencies)

        # Save the generated code to the dynamic folder
        file_path = os.path.join(DYNAMIC_FOLDER, filename)
        write_file(file_path, generated_code)
        update_change_log(
            file_path, generated_code, action="create", functionality=functionality
        )

        # Add the filename and its corresponding code to the dictionary
        code_files[filename] = generated_code

    # Update the session state with the new code files
    update_dynamic_files()


def initialize_dynamic_main():
    """
    Ensures that the DYNAMIC_MAIN file is initialized.
    """

    dynamic_main_path = os.path.join(DYNAMIC_FOLDER, DYNAMIC_MAIN)

    if not os.path.exists(dynamic_main_path):
        file_contents = """def main():
            try:
                return "Hello from dynamic_main.py"
            except Exception as e:
                print(f'An error occurred: {e}')

        if __name__ == '__main__':
            main()"""
        write_file(dynamic_main_path, file_contents)
        logger.info(f"Initialized {dynamic_main_path}")
    else:
        logger.info(f"Found {dynamic_main_path}")


def get_code_content_and_main_file():
    """
    Function to get the content and path of the main code file from the specified directory.
    """
    ensure_dynamic_directory()  # Ensure the directory exists

    code_files = list_files(DYNAMIC_FOLDER)

    if len(code_files) == 0:
        return None, None  # No Python files found

    main_file_path = os.path.join(DYNAMIC_FOLDER, DYNAMIC_MAIN)

    code_content = read_file(main_file_path)

    return code_content, main_file_path


def fetch_code_for_improvement(
    objective: str, expected_result: str, result: str, error: str
) -> (Union[str, None], Union[str, None], Union[str, None], Union[str, None]):
    """
    Determine what part of the code should be sent for improvement.

    Parameters:
    code_files (list): List of file paths as strings representing existing code files.

    Returns:
    Tuple containing the code content as a string and the file path as a string.
    """

    last_change = get_last_change_log_entry()

    # Generate a prompt to ask the language model for the file and action to take on it
    file_prompt = build_action_selection_prompt(
        objective, error, result, expected_result, last_change
    )

    # Get the code from the language model
    code_response = get_code(file_prompt, response_type="json")

    try:
        # Safely parse the response to get the generated code
        parsed_response = json.loads(code_response)
        file_path = parsed_response["file"]
        action = parsed_response["action"]
        functionality = parsed_response["functionality"]
        code_content = None

        if action == "edit":
            code_content = read_file(file_path)

        return file_path, action, code_content, functionality

    except (json.JSONDecodeError, KeyError):
        logger.error(f"Received an invalid JSON response for the file path. Skipping.")

    return None, None, None, None


def make_improvements(
    objective: str, expected_result: str, result: str, error: str
) -> None:
    # Feth the code that needs improvement
    file_path, action, code_content, functionality = fetch_code_for_improvement(
        objective, expected_result, result, error
    )

    if DYNAMIC_FOLDER not in file_path:
        logger.error(
            "Code to improve not in dynamic folder. Exiting program for safety."
        )
        logger.error(json.dumps(get_last_run_log_entry(), indent=4))
        return False

    logger.info(f"File: {file_path}, Action: {action}")

    improved_code = None
    all_files = str(list_files(DYNAMIC_FOLDER))

    # create, edit, or delete.
    if action == "edit":
        prompt = IMPROVE_PROMPT.format(
            objective=objective,
            expected_result=expected_result,
            result=result,
            error=error,
            code_content=code_content,
            all_files=all_files,
            file_path=file_path,
            functionality=functionality,
        )
        improved_code = get_code(prompt, response_type="code")

    elif action == "create":
        prompt = CREATE_PROMPT.format(
            objective=objective,
            expected_result=expected_result,
            result=result,
            error=error,
            all_files=all_files,
            file_path=file_path,
            functionality=functionality,
        )

        improved_code = get_code(prompt, response_type="code")

    elif action == "delete":
        delete_file(file_path)
        update_change_log(file_path, None, action="delete", functionality=functionality)

    else:
        raise ValueError(f"Unknown action: {action}")

    if improved_code:
        dependencies = get_code_dependencies(improved_code)

        if dependencies:
            check_and_install_dependencies(dependencies)

        # Update codebase with the improved code
        update_code(improved_code, file_path)
        update_change_log(
            file_path, improved_code, action=action, functionality=functionality
        )


def update_code(new_code: str, file_path: str) -> None:
    """
    Update the codebase with the new code received.

    Parameters:
    new_code (str): The new code to replace the old one.
    file_path (str): The path to the file to update.
    """
    write_file(file_path, new_code)

    # Update the session state with the new code files
    update_dynamic_files()


def objective_is_met() -> Tuple[bool, Union[str, None], Union[str, None]]:
    config_data = read_session_config()

    try:
        # Fetch code content
        code, _ = get_code_content_and_main_file()
        if not code:
            raise ValueError("No code found in the dynamic main file.")

        # Run Python script in a separate process
        file_path = os.path.join(DYNAMIC_FOLDER, DYNAMIC_MAIN)
        process = subprocess.Popen(
            ["python", file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        output, error_trace = process.communicate()

        if process.returncode != 0:
            update_run_log(config_data, "objective_is_not_met_error", None, error_trace)
            return False, None, error_trace

        _, expected_result, _ = get_session()

        logger.info("Objective Result:", output, "Expected Results:", expected_result)

        if str(output.strip()) == str(expected_result.strip()):
            update_run_log(config_data, "objective_is_met", str(output.strip()), None)
            return True, str(output.strip()), None
        else:
            update_run_log(
                config_data, "objective_is_not_met", str(output.strip()), None
            )
            return False, str(output.strip()), None

    except Exception as e:
        error_trace = str(e)
        update_run_log(config_data, "objective_is_not_met_error", None, error_trace)
        return False, None, error_trace
