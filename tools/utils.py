from typing import List


def command_args_to_str(command: List[str]):
    command_len = len(command)
    if command_len == 1:
        return ""
    start_args_index = 1
    end_args_index = command_len
    args_str = " ".join(
        command[start_args_index:end_args_index]
    )
    return args_str
