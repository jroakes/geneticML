# GeneticML

## Description

GeneticML is a Python project aimed at automatically refining Python code to meet a specified objective. The project uses a large language model to make incremental improvements in the code base and evaluates the changes in a continual testing cycle until the objective is met or found to be unachievable.

# Example Run

```
(base) C:\Projects\geneticML>python geneticML/main.py

🤖: Do you want to restart the configuration? [y/n]: y
🤖: Please specify the objective:
Program that returns the latest stock price of Apple

🤖: Please specify the expected result for this objective:
180.19

2023-08-29 08:14:47.725 | INFO     | code_manager:initialize_dynamic_main:109 - Initialized dynamic_main\dynamic_main.py
2023-08-29 08:15:02.087 | INFO     | code_manager:make_improvements:187 - File: dynamic_main\dynamic_main.py, Action: edit
2023-08-29 08:15:12.289 | INFO     | code_manager:objective_is_met:282 - Objective Result:
2023-08-29 08:15:12.293 | INFO     | __main__:main_loop:69 - Got the following result: An error occurred: 'regularMarketPrice'
None
2023-08-29 08:15:12.295 | INFO     | __main__:main_loop:70 - Got the following error: None
2023-08-29 08:15:12.297 | INFO     | __main__:main_loop:75 - Objective not met. Making improvements.
2023-08-29 08:15:20.781 | INFO     | code_manager:make_improvements:187 - File: dynamic_main\dynamic_main.py, Action: edit
2023-08-29 08:15:35.007 | INFO     | code_manager:objective_is_met:282 - Objective Result:
2023-08-29 08:15:35.011 | INFO     | __main__:main_loop:69 - Got the following result: An error occurred: 'regularMarketPrice'
None
2023-08-29 08:15:35.013 | INFO     | __main__:main_loop:70 - Got the following error: None
2023-08-29 08:15:35.014 | INFO     | __main__:main_loop:75 - Objective not met. Making improvements.
2023-08-29 08:15:54.276 | INFO     | code_manager:make_improvements:187 - File: dynamic_main\dynamic_main.py, Action: edit
2023-08-29 08:16:12.422 | INFO     | code_manager:objective_is_met:282 - Objective Result:
2023-08-29 08:16:12.427 | INFO     | __main__:main_loop:69 - Got the following result: The key regularMarketPrice does not exist in the stock info.
None
2023-08-29 08:16:12.428 | INFO     | __main__:main_loop:70 - Got the following error: None
2023-08-29 08:16:12.430 | INFO     | __main__:main_loop:75 - Objective not met. Making improvements.
2023-08-29 08:16:27.668 | INFO     | code_manager:make_improvements:187 - File: dynamic_main\dynamic_main.py, Action: edit
2023-08-29 08:16:40.479 | INFO     | code_manager:objective_is_met:282 - Objective Result:
2023-08-29 08:16:40.484 | INFO     | __main__:main_loop:69 - Got the following result: 180.19000244140625
2023-08-29 08:16:40.486 | INFO     | __main__:main_loop:70 - Got the following error: None
2023-08-29 08:16:40.488 | INFO     | __main__:main_loop:75 - Objective not met. Making improvements.
2023-08-29 08:16:55.037 | INFO     | code_manager:make_improvements:187 - File: dynamic_main\dynamic_main.py, Action: edit
2023-08-29 08:17:08.441 | INFO     | code_manager:objective_is_met:282 - Objective Result:
2023-08-29 08:17:08.446 | INFO     | __main__:main_loop:69 - Got the following result: 180.19
2023-08-29 08:17:08.448 | INFO     | __main__:main_loop:70 - Got the following error: None
2023-08-29 08:17:08.450 | SUCCESS  | __main__:main_loop:72 - Objective met. Exiting program.
```


## Installation

1. Clone the repository.
    ```bash
    git clone https://github.com/jroakes/GeneticML.git
    ```

2. Navigate into the project directory.
    ```bash
    cd GeneticML
    ```

3. Install the required packages.
    ```bash
    pip install -r requirements.txt
    ```

## Directory Structure

```
GeneticML\
|-- config.json
|-- requirements.txt
|-- src\
|   |-- main.py
|   |-- code_manager.py
|   |-- dependency_manager.py
|   |-- interaction_manager.py
|   |-- session_manager.py
|   |-- taxonomyml_interface.py
|   |-- utils\
|       |-- constants.py
|       |-- file_operations.py
|       |-- prompts.py
|       |-- string_operations.py
|-- dynamic_main\
```

## Main Components

### `main.py`

This is the entry point for the application. It orchestrates the entire program logic including session management, user interaction, and code improvement cycles.

- `initialize_dynamic(objective: str)`: Initializes the dynamic environment.
- `maybe_restart_config()`: Checks if the user wants to restart the configuration.
- `main_loop()`: Main processing loop.

For more details, [see `main.py`](./src/main.py).

### `code_manager.py`

Manages the code generation, evaluation, and improvements.

### `interaction_manager.py`

Manages all user interactions, including collecting the objective and any necessary permissions.

### `session_manager.py`

Manages session data and config.

### `taxonomyml_interface.py`

Interface to the large language model for code improvements.

### `utils`

Utility functions and constants.

## How to Run

1. Set your OpenAI key.
    ```bash
    export OPENAI_API_KEY=sk-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    ```
    or windows
    ```bash
    set OPENAI_API_KEY=sk-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    ```

2. Run `main.py`.
    ```bash
    python geneticML/main.py
    ```

## Contributing

If you'd like to contribute, please fork the repository and use a feature branch. Pull requests are warmly welcome.

## License

MIT
