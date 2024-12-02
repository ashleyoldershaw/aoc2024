def read_file(file_name: str):
    """
    Return the contents of a file

    :param file_name:
    :return file contents:
    """
    with open(file_name, "r") as f:
        return f.read()
