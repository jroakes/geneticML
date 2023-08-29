
import os

from utils.constants import DYNAMIC_FOLDER, DYNAMIC_MAIN
from utils.file_operations import read_file, list_files


OUTLINE_PROMPT = """Outline the files and functionalities needed to achieve the objective: `{objective}`.
    The main file should be named `{DYNAMIC_MAIN}`. The main function should be named `main()`. `main()` will be called to test your code.
    DO NOT include any code or libraries that require API keys or other sensitive information.
    Include any information about dependencies in the functionality description.
    Output should be a valid JSON object with filenames as keys and their corresponding functionalities as values.
    """

FILE_PROMPT = """Generate the code for `{filename}` to implement the following functionality: `{functionality}`
        Output should be a valid JSON object with the key `code` and the value as the generated code.
        """


IMPROVE_PROMPT = """Improve the following Python code to that is part of a program designed to achieve the objective: '{objective}'.

        - Expected program result: 
        {expected_result}

        - Last program result: 
        {result}

        - Last program error: 
        {error}

        - Functionality changes required (if any): 
        {functionality}

        - All program filenames:
        {all_files}

        - The filename for this code: 
        {file_path}

        - Code to improve:
        {code_content}
        
        - Improved code for file:
        """


CREATE_PROMPT = """Create the following Python code to that is part of a program designed to achieve the objective: '{objective}'.
        - Expected program result: 
        {expected_result}
        
        - Last program result:
        {result}

        Last program error:
        {error}

        - Functionality required: 
        {functionality}

        - All program filenames:
        {all_files}

        - The filename for this code: 
        {file_path}

        Code for file:"""





def build_action_selection_prompt(objective: str, error: str = None, result: str = None, expected_result: str = None, last_change: dict = None) -> str:
        """
        Build a prompt to ask the language model to select a file and an action to take on it."""

        # Get all files in the dynamic folder
        all_files = list_files(DYNAMIC_FOLDER)

        last_changed_file = last_change.get("file_path", None)
        last_changed_action = last_change.get("action", None)
        last_changed_functionality = last_change.get("functionality", None)
    
        # Generate a prompt to ask the language model to generate code for each file
        file_prompt = f"""I am developing a Python program with the following objective: 
        {objective}.

        - The main file of the program (entrypoint): 
        {DYNAMIC_MAIN}.

        - The main file's code: 
        {read_file(os.path.join(DYNAMIC_FOLDER, DYNAMIC_MAIN))}.

        - All program filenames:
        {all_files}
        """

        if error:
                file_prompt += f"""
                - Last program error:
                {error}

                """
        
        if result:
                file_prompt += f"""
                - Expected program result: 
                {expected_result}
                
                - Last program result:
                {result}
                """
        
        if last_changed_file:
                file_prompt += f"""
                - Here is the last file change you requested: 
                {last_changed_action} {last_changed_file}

                - The functionality you requested for the file:
                {last_changed_functionality}

                These changes were already implemented.
                
                """

        file_prompt += f"""Please select a new file to take action on to meet the objective
        Actions include: create, edit, or delete.
        The output should be a valid JSON object with:
                - The key `file` and the value as the file path (string).
                - The key `action` and the value as the action to take on the file (string).
                - The key `functionality` and the value as the functionality instructions to create or edit in the file (string)."""
        
        return file_prompt