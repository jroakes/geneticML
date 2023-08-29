from loguru import logger

from session_manager import get_session, set_session, create_session_config
from code_manager import make_improvements, objective_is_met, ensure_dynamic_directory, initialize_dynamic_main, delete_dynamic_directory
from interaction_manager import ask_user_for_objective, ask_user_for_permission


from utils.constants import DYNAMIC_FOLDER


def initialize_dynamic(objective: str):
    # Create the dynamic folder if it doesn't exist
    ensure_dynamic_directory()
    # Initialize the dynamic main file
    initialize_dynamic_main()
    # Create the outline and files if they don't exist
    # TODO: Skipping for now as it creates files that are not needed
    # create_outline_and_files(objective)


def maybe_restart_config():
    """
    Check if the user wants to restart the configuration.
    """
    user_permission = ask_user_for_permission("Do you want to restart the configuration?")
    if user_permission:
        delete_dynamic_directory()
        create_session_config()
        return True
    return False



def main_loop():
    """
    Orchestrates the entire program logic.
    """
    # Get session data
    objective, expected_result, code_files = get_session()
    met = False
    error = None
    result = None

    if code_files and len(code_files) > 0:
        if maybe_restart_config():
            objective, expected_result, code_files = get_session()

    if not objective:
        objective, expected_result = ask_user_for_objective()
        set_session(objective, expected_result)

    if not code_files:
        initialize_dynamic(objective)

    met, result, error = objective_is_met()
    if met:
        logger.success("Objective met. Exiting program.")
        return True
        
    # Main processing loop
    while True:

        # Make code improvements
        make_improvements(objective, expected_result, result, error)

        # Check if the objective is met
        met, result, error = objective_is_met()

        logger.info(f"Got the following result: {result}")
        logger.info(f"Got the following error: {error}")
        if met:
            logger.success("Objective met. Exiting program.")
            return True
        else:
            logger.info("Objective not met. Making improvements.")



if __name__ == "__main__":
    main_loop()
