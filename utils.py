from pathlib import Path


def read_file(file_name: Path):
    """
    Return the contents of a file

    :param file_name:
    :return file contents:
    """
    with open(str(file_name), "r") as f:
        return f.read().strip()
