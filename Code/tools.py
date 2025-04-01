import ipaddress

def insert_line(filename, index_line: int, data: str) -> None:
    """
    Insère une ligne de données à un index spécifique dans un fichier.
    Args:
        filename (str): Le chemin du fichier où insérer la ligne.
        index_line (int): L'index de la ligne où insérer les données.
        data (str): La ligne de données à insérer.
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
        int: L'index de la ligne dans le fichier.
    """
    with open(filename, 'r') as file:
        lines = file.readlines()
    return lines.index(line)

get_subnet = lambda ip_with_cidr: str(ipaddress.ip_network(ip_with_cidr, strict=False).network_address)
"""
Renvoie l'adresse réseau (subnet) pour une adresse IP avec notation CIDR.
Args:
    ip_with_cidr (str): L'adresse IP avec notation CIDR (ex. "192.168.2.1/24").
Returns:
    str: L'adresse réseau correspondante (ex. "192.168.2.0").
"""

def get_reversed_mask(ip_with_cidr: str) -> str:
    """
    Renvoie le masque de sous-réseau inversé pour une adresse IP avec notation CIDR.
    Args:
        ip_with_cidr (str): L'adresse IP avec notation CIDR (ex. "192.168.2.1/30").
    Returns:
        str: Le masque de sous-réseau inversé (ex. "0.0.0.4").
    """
    network = ipaddress.ip_network(ip_with_cidr, strict=False)
    reversed_mask = ~int(network.netmask) & 0xFFFFFFFF
    return str(ipaddress.IPv4Address(reversed_mask))

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
