from tools import insert_line, find_index, is_border_router, generate_addresses_dict, give_subnet_dict, give_subnet_interconnexion, get_subnet_interconnexion


def create_base_cfg(base_config: list, router: str) -> None:
    """
    Creates the base config file named iX_startup-config.cfg with X being the number/name of the router.
    Args:
        base_config (list): The base configuration lines.
        router (str): The router identifier.
    The file contains all the lines from the base_config list plus the hostname of the router.
    """
    # Writes the base_config in the config file
    with open(f'i{router[1:]}_startup-config.cfg', 'w') as file:
        for entry in base_config:
            file.write(entry + '\n')
    # Writes the hostname in the config file
    insert_line(router, 3, f"hostname {router}\n")

def create_loopback_interface(router: str) -> None:
    """
    Insert the loopback lines at the right place in the config file of a given router.
    Args:
        router (str): The router identifier.
    """
    # Finds the index of where to insert the loopback part
    index_line = find_index(router, "ip tcp synwait-time 5\n")
    # Insert the loopback part
    insert_line(router, index_line, f"interface Loopback0\n no ip address\n ipv6 address 2001::{router[1:]}/128\n ipv6 enable\n")

def create_interfaces(router: str, topology: dict, AS: str) -> None:
    """
    Generate the interfaces with the correct IPv6 addresses for each router of each AS.
    Args:
        router (str): The router identifier.
        topology (dict): The network topology.
        AS (str): The AS identifier.
    """
    # Generate the addresses dictionary
    addresses_dict = generate_addresses_dict(topology)
    # Finds the line where to insert the interface
    index_line = find_index(router, line="ip tcp synwait-time 5\n")
    # Iterate over each neighbor in the addresses dictionary
    for neighbor_info in addresses_dict[router]:
        for neighbor, details in neighbor_info.items():
            interface, ipv6_address, neighbor_AS = details
            # Insert the lines in the config files for the interface
            insert_line(router, index_line,
                f"interface {interface}\n"                                                  # Interface name
                f" no ip address\n"                                                         # Disable IPv4 addressing
                f" negotiation auto\n"                                                      # Enable automatic negotiation for the interface
                f" ipv6 address {ipv6_address}\n"                                           # Assign an IPv6 address
                f" ipv6 enable\n"                                                           # Enable IPv6 on the interface
            )
            # Increment the index line
            index_line += 5
