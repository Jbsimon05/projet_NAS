import ipaddress

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

##############################################################################

def example_tool_function(param: str) -> str:
    """
    Exemple de fonction outil.
    Args:
        param (str): Une chaîne de caractères en entrée.
    Returns:
        str: Une chaîne de caractères modifiée.
    """
    return f"Processed: {param}"

def main():
    """
    Fonction principale pour tester les outils.
    """
    print("Testing tools...")
    result = example_tool_function("Test input")
    print(f"Result: {result}")

if __name__ == "__main__":
    main()


get_subnet = lambda ip_with_cidr: str(ipaddress.ip_network(ip_with_cidr, strict=False).network_address)

def get_reversed_mask(ip_with_cidr: str) -> str:
    """
    Returns the reversed subnet mask for a given IP address with CIDR notation.
    Args:
        ip_with_cidr (str): The IP address in CIDR notation (e.g., "192.168.2.1/30").
    Returns:
        str: The reversed subnet mask (e.g., "0.0.0.4").
    """
    network = ipaddress.ip_network(ip_with_cidr, strict=False)
    reversed_mask = ~int(network.netmask) & 0xFFFFFFFF
    return str(ipaddress.IPv4Address(reversed_mask))