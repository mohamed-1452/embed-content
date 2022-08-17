from typing import Callable, List, Tuple, TypeVar
from os.path import normpath, isdir, isfile, splitext
from glob import glob


T = TypeVar('T')


def ask(
    query: str,
    validators: List[Callable[[str], Tuple[bool, str]]] = [],
    transformer: Callable[[str], T] = lambda x: x,
):
    while True:
        answer = input(query)
        passed = True

        for validator in validators:
            valid, message = validator(answer)
            if not valid:
                print(message)
                passed = False
                break

        if not passed:
            continue

        return transformer(answer)


# Validators
def is_numeric(text: str):
    valid = text.isnumeric()
    return (valid, "input must be numeric")


def is_float(text: str):
    valid = True
    try:
        float(text)
    except ValueError:
        valid = False
    return (valid, "input must be a float")


def is_greater_than_zero(text: str):
    return (float(text) > 0, "input must be greater than 0")


def is_dir(text: str):
    valid = isdir(text)
    return (valid, "input must be a valid directory")


def is_content_path(text: str):
    allowed_ext = ['.jpg', '.jpeg', '.png', '.mp4']
    valid = True
    if isfile(text):
        valid = splitext(text)[1] in allowed_ext
    elif isdir(text):
        path = text_to_dir_path(text)
        matches = False
        for ext in allowed_ext:
            if len(glob(path + '*' + ext)) > 0:
                matches = True
                break
        if not matches:
            valid = False
    else:
        valid = False
    return (valid, "input must be a valid content path")


def is_embed_path(text: str):
    allowed_ext = ['.jpg', '.jpeg', '.png']
    valid = isfile(text) and splitext(text)[1] in allowed_ext
    return (valid, "input must be a valid embed file")


def is_horizontal_position(text: str):
    valid = True if text in ['left', 'right'] else False
    return (valid, "input must be a valid horizontal position")


def is_vertical_position(text: str):
    valid = True if text in ['top', 'bottom'] else False
    return (valid, "input must be a valid vertical position")


# Transformers
def text_to_int(text: str):
    return int(text)


def text_to_float(text: str):
    return float(text)


def text_to_dir_path(text: str):
    return normpath(text) + '/'


def text_to_file_path(text: str):
    return normpath(text)


def text_to_content_paths(text: str):
    if isfile(text):
        return [text_to_file_path(text)]
    allowed_ext = ['.jpg', '.jpeg', '.png', '.mp4']
    dir_path = text_to_dir_path(text)
    files = []
    for ext in allowed_ext:
        files += [path for path in glob(dir_path + '*' + ext)]
    return files
