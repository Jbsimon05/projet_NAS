import ipaddress
from ipaddress import IPv4Interface
import math

def insert_line(filename, index_line: int, data: str) -> None:
    """
    Insère une ligne de texte à un index spécifique dans un fichier.
    
    Args:
        filename (str): Le chemin du fichier où insérer la ligne.
        index_line (int): L'index de la ligne où insérer les données (commence à 0).
        data (str): La ligne de texte à insérer.
    """
    with open(filename, 'r') as file:
        lines = file.readlines()
    lines.insert(index_line, data)
    with open(filename, 'w') as file:
        file.writelines(lines)

def find_index(filename, line: str) -> int:
    """
    Trouve l'index d'une ligne spécifique dans un fichier.
    
    Args:
        filename (str): Le chemin du fichier à analyser.
        line (str): La ligne à rechercher dans le fichier.
    
    Returns:
        int: L'index de la ligne dans le fichier (commence à 0).
    """
    with open(filename, 'r') as file:
        lines = file.readlines()
    return lines.index(line)


import ipaddress

def extract_ip_address(cidr_notation: str) -> str:
    """
    Extracts the IP address from a CIDR notation string.

    Args:
        cidr_notation (str): The IP address in CIDR notation (e.g., '192.168.1.1/24').

    Returns:
        str: The extracted IP address (e.g., '192.168.1.1').
    """
    return str(ipaddress.ip_interface(cidr_notation).ip)

def get_subnet_mask(cidr_notation: str) -> str:
    """
    Retrieves the subnet mask from a CIDR notation string.

    Args:
        cidr_notation (str): The IP address in CIDR notation (e.g., '192.168.1.1/24').

    Returns:
        str: The subnet mask corresponding to the CIDR prefix length (e.g., '255.255.255.0').
    """
    return str(ipaddress.ip_network(cidr_notation, strict=False).netmask)

def get_wildcard_mask(cidr_notation: str) -> str:
    """
    Computes the wildcard mask, which is the bitwise inverse of the subnet mask, from a CIDR notation string.

    Args:
        cidr_notation (str): The IP address in CIDR notation (e.g., '192.168.1.1/24').

    Returns:
        str: The wildcard mask (e.g., '0.0.0.255').
    """
    subnet_mask = get_subnet_mask(cidr_notation)
    # Convert subnet mask to binary, invert bits, and convert back to dotted decimal format
    wildcard_mask = '.'.join(str(255 - int(octet)) for octet in subnet_mask.split('.'))
    return wildcard_mask

def get_router_name(config: str) -> str:
    """
    Extrait le nom du routeur à partir de la configuration.
    
    Args:
        config (str): La configuration du routeur sous forme de chaîne.
    
    Returns:
        str: Le nom du routeur.
    """
    lines = config.splitlines()
    for line in lines:
        if line.startswith("hostname"):
            return line.split()[1]
    return None

add_ip = lambda ip_cidr, n: str(IPv4Interface(intf := IPv4Interface(ip_cidr)).ip + n) + '/' + str(intf.network.prefixlen)

get_subnet = lambda ip_cidr: str(IPv4Interface(ip_cidr).network.network_address)

##############################################################################

def main():
    """
    Fonction principale pour tester les outils.
    """
    # Création ou vidage du fichier test_config.cfg
    with open("test_config.cfg", "w") as file:
        file.write("Ligne 1\nLigne 2\nLigne 3\n")

    print("Test des outils...")

    # Test de la fonction insert_line
    print("Test de insert_line :")
    try:
        insert_line("test_config.cfg", 2, "Nouvelle ligne\n")
        print("insert_line exécutée avec succès.")
    except Exception as e:
        print(f"Erreur dans insert_line : {e}")

    # Test de la fonction find_index
    print("\nTest de find_index :")
    try:
        index = find_index("test_config.cfg", "Nouvelle ligne\n")
        print(f"find_index a trouvé l'index : {index}")
    except Exception as e:
        print(f"Erreur dans find_index : {e}")

    # Test de la fonction get_subnet
    print("\nTest de get_subnet :")
    try:
        subnet = get_subnet("192.168.2.1/24")
        print(f"get_subnet a renvoyé : {subnet}")
    except Exception as e:
        print(f"Erreur dans get_subnet : {e}")

    # Test de la fonction get_reversed_mask
    print("\nTest de get_reversed_mask :")
    try:
        reversed_mask = get_reversed_mask("192.168.2.1/30")
        print(f"get_reversed_mask a renvoyé : {reversed_mask}")
    except Exception as e:
        print(f"Erreur dans get_reversed_mask : {e}")

if __name__ == "__main__":
    main()
