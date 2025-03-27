def insert_line(router: str, index_line: int, data: str) -> None:
    """
    For a given router, insert the data at index_line in its config file.
    Args:
        router (str): The router identifier.
        index_line (int): The line index where the data should be inserted.
        data (str): The data to be inserted.
    """
    # Get the lines in the file and insert the new one
    with open(f"i{router[1:]}_startup-config.cfg", 'r') as file :
        lines = file.readlines()
        lines.insert(index_line, data)
    # Writes the updated list in the file
    with open(f"i{router[1::]}_startup-config.cfg", 'w') as file :
        file.writelines(lines)

def find_index(router: str, line: str) -> int:
    """
    For a given router, finds the index of a given line in its config file.
    Args:
        router (str): The router identifier.
        line (str): The line to find in the config file.
    Returns:
        int: The index of the line in the config file.
    """
    current_index = 1
    with open(f'i{router[1:]}_startup-config.cfg', 'r') as file:
        # Browses the lines to find the wanted one
        l = file.readline()
        while l != line:
            l = file.readline()
            current_index += 1
    return current_index


is_border_router = lambda router : router[-2:] == "PE"
