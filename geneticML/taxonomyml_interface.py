import os
import tiktoken

from numba.core.errors import NumbaDeprecationWarning, NumbaPendingDeprecationWarning
import warnings
warnings.simplefilter('ignore', category=NumbaDeprecationWarning)
warnings.simplefilter('ignore', category=NumbaPendingDeprecationWarning)

from taxonomyml.lib.api import get_openai_response_chat
from utils.file_operations import update_prompt_log
from utils.constants import MAX_TOKENS, OPENAI_MODEL

# Get OPENAI_API_KEY from environment variables
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

def count_tokens(text: str, model_name='gpt-4'):
    """Returns the number of tokens in a text string."""

    encoding = tiktoken.encoding_for_model(model_name)
    num_tokens = len(encoding.encode(text))

    return num_tokens


def get_code(prompt: str, response_type: str = "code") -> str:
    """
    Send a prompt to get_openai_response_chat and receive code.

    Parameters:
    - prompt (str): The prompt to be sent to get_openai_response_chat, should be <= 8k tokens.

    Returns:
    str: The improved code returned by get_openai_response_chat.
    """

    prompt_len = count_tokens(prompt, OPENAI_MODEL)

    if prompt_len > MAX_TOKENS:
        raise ValueError(f"The prompt exceeds the {OPENAI_MODEL} token limit.")
    
    if response_type == "code":
        system_message = "You are a world-class expert at Python programming.  You always create production-ready and error free code. Your response MUST be ONLY valid Python code and no other text. Ensure all libraries are well-maintained and production-ready. DO NOT Use any samples or example code. DO NOT use markdown in your response."
    elif response_type == "json":
        system_message = "You are a world-class expert at Python programming.  Your goal is production-ready and error free code. Your response MUST be in valid JSON format according to the instructions. For any suggestions you provide, ensure all libraries are well-maintained and production-ready. Avoid asking for any changes that require API keys or other information that is not provided. DO NOT Use any samples or example code."
    else:
        raise ValueError(f"Invalid response_type: {response_type}")
    
    update_prompt_log(prompt)
    
    new_code = get_openai_response_chat(prompt, model = OPENAI_MODEL, system_message = system_message, openai_api_key = OPENAI_API_KEY)

    return new_code
