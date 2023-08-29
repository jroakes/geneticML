from datetime import datetime
from typing import Tuple, List, Dict, Any, Union

from utils.file_operations import read_config, write_config, create_config, list_files
from utils.constants import DYNAMIC_FOLDER


def read_session_config() -> Dict:
    return read_config()


def write_session_config(data: Dict) -> None:
    write_config(data)


def create_session_config() -> None:
    create_config()


def get_session() -> Tuple[str, str, List[str]]:
    config_data = read_session_config()
    return (config_data.get('last_known_objective', ''), 
            config_data.get('last_known_expected_result', ''), 
            config_data.get('code_files', []))


def set_session(objective: str, expected_result: str) -> None:
    config_data = read_session_config()
    config_data['last_known_objective'] = objective
    config_data['last_known_expected_result'] = expected_result
    config_data['code_files'] = list_files(DYNAMIC_FOLDER)
    write_session_config(config_data)


def update_change_log(file_path: str, code: str, action: str = None, functionality: str = None) -> None:
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    config_data = read_session_config()
    change_log = config_data.get('change_log', [])
    change_log.append({
        'file_path': file_path,
        'action': action,
        'functionality': functionality,
        'code': code,
        'timestamp': timestamp
    })
    config_data['change_log'] = change_log
    write_session_config(config_data)


def get_last_run_log_entry() -> Dict:
    config_data = read_session_config()
    run_log = config_data.get('run_log', [])
    if len(run_log) > 0:
        return run_log[-1]
    return {}

def get_last_change_log_entry() -> Dict:
    config_data = read_session_config()
    change_log = config_data.get('change_log', [])
    if len(change_log) > 0:
        return change_log[-1]
    return {}


def update_run_log(config_data: Dict, test: str, result: Any, error: Union[str, None]) -> None:
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    run_log = config_data.get('run_log', [])
    run_log.append({
        'test': test,
        'timestamp': timestamp,
        'result': result,
        'error': error
    })
    config_data['run_log'] = run_log
    write_session_config(config_data)


def update_dynamic_files() -> None:
    config_data = read_session_config()
    config_data['code_files'] = list_files(DYNAMIC_FOLDER)
    write_session_config(config_data)


