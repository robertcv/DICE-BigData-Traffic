import time
import os

"""
Here are some useful functions for working with files.
"""


def old_or_not_exists(file, age):
    """
    This function tests if the file exists. If it does, then we check when it
    was last modified. This helps with checking if we have a not too old copy of
    data in a local file.

    Args:
        file (file): File object.
        age (int): Number of seconds.

    Returns:
        bool: If the file dose not exist or is older then age seconds True else
            False.

    """
    if not os.path.isfile(file):
        return True
    last_modified = os.path.getmtime(file)
    now = time.time()
    return now - last_modified > age


def file_path(source_file_path, file_path):
    """
    This function appends the relative file_path to the absolute path from
    source_file_path.

    Args:
        source_file_path (str): Starting file location.
        file_path (str): Relative file location.

    Returns:
        str: Absolute location of file_path.

    """
    return os.path.join(os.path.dirname(os.path.realpath(source_file_path)),
                        file_path)


def make_dir(directory):
    """
    This function creates a directory.

    Args:
        directory: Directory we want to create.

    """
    os.makedirs(os.path.dirname(directory), exist_ok=True)

