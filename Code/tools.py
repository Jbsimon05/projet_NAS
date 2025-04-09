import ipaddress
from ipaddress import IPv4Interface


def get_subnet(cidr_notation: str) -> str:
    """
    Computes the network address from an IP address in CIDR notation.

    Args:
        cidr_notation (str): The IP address in CIDR notation (e.g., '192.168.1.1/24').

    Returns:
        str: The network address (e.g., '192.168.1.0').
    """
    network = ipaddress.ip_network(cidr_notation, strict=False)
    return str(network.network_address)

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
