def insert_line(filename, index_line: int, data: str) -> None:
    """
    Insère une ligne de données à un index spécifique dans le fichier de configuration.
    Args:
        index_line (int): L'index de la ligne où insérer les données.
    """
    with open(filename, 'r') as file:
        lines = file.readlines()
    lines.insert(index_line, data)
    with open(filename, 'w') as file:
        file.writelines(lines)

def find_index(filename, line: str) -> int:
    """
    Trouve l'index d'une ligne spécifique dans le fichier de configuration.
    Args:
        line (str): La ligne à rechercher dans le fichier de configuration.
    Returns:
        int: L'index de la ligne dans le fichier de configuration.
    """
    with open(filename, 'r') as file:
        lines = file.readlines()
    return lines.index(line)
