import sys
from loguru import logger


def ask_user_for_objective() -> tuple:
    """
    Collects objective and expected result from the user.

    Returns:
    Tuple containing:
    - objective (str): The objective specified by the user.
    - expected_result (str): The expected result specified by the user.
    """
    print("🤖:", "Please specify the objective:")
    objective = input()
    
    print("🤖:", "Please specify the expected result for this objective:", )
    expected_result = input()
    
    return objective, expected_result



def ask_user_for_permission(prompt: str) -> bool:
    """
    General function to ask for user permissions.

    Parameters:
    - prompt (str): The question to ask the user.

    Returns:
    bool: True if the user gives permission, otherwise False.
    """
    response = input(f"🤖: {prompt} [y/n]: ").strip().lower()

    while response not in ['y', 'n']:
        print("🤖:", "Invalid response. Please answer with 'y' for yes or 'n' for no.")
        response = input(f"{prompt} [y/n]: ").strip().lower()
    
    return response == 'y'
