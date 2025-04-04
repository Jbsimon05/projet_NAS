import ipaddress
import math

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


def get_subnet(ip_with_suffix: str) -> str:
    ip_part, suffix = ip_with_suffix.split('/')
    suffix = int(suffix)
    ip_octets = list(map(int, ip_part.split('.')))

    # Convertir l'adresse IP en entier 32 bits
    ip_int = (ip_octets[0] << 24) | (ip_octets[1] << 16) | (ip_octets[2] << 8) | ip_octets[3]

    # Calcul du nombre de bits à mettre à 0 (log2 de la valeur du suffixe)
    zero_bits = int(math.log2(suffix))
    mask = ~((1 << zero_bits) - 1) & 0xFFFFFFFF

    # Appliquer le masque
    subnet_int = ip_int & mask

    # Reconvertir en format IPv4
    subnet_ip = '.'.join(str((subnet_int >> (8 * i)) & 0xFF) for i in reversed(range(4)))
    return subnet_ip


def get_mask(bits_to_clear: str) -> str:
    """
    Returns a custom subnet mask where the rightmost `bits_to_clear` bits are set to 0,
    and the remaining (leftmost) bits are set to 1.
    """
    bits_to_clear = int(bits_to_clear.split('/')[1]) if '/' in bits_to_clear else bits_to_clear
    if not (0 <= bits_to_clear <= 32):
        raise ValueError("bits_to_clear must be between 0 and 32")
    
    one_bits = 32 - bits_to_clear
    mask = (0xFFFFFFFF >> (32 - one_bits)) << (32 - one_bits)
    
    return '.'.join(str((mask >> (8 * i)) & 0xFF) for i in reversed(range(4)))

def get_reversed_mask(bits_to_clear: str) -> str:
    """
    Returns the bitwise inverse of the result from get_mask.
    """
    # Call get_mask and parse the result
    mask_str = get_mask(bits_to_clear)
    mask_parts = [int(part) for part in mask_str.split('.')]
    
    # Convert to 32-bit integer
    mask_int = sum(part << (8 * (3 - i)) for i, part in enumerate(mask_parts))
    
    # Invert and convert back to dotted decimal
    reversed_int = ~mask_int & 0xFFFFFFFF
    return '.'.join(str((reversed_int >> (8 * i)) & 0xFF) for i in reversed(range(4)))

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
