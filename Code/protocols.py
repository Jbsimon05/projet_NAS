from tools import insert_line, find_index
import json

def activate_bgp(routeur: str, topology: dict, AS: str) -> None:
    """
    Activates BGP on the given router using the Loopback addresses of its neighbors.
    Args:
        routeur (str): The router identifier.
        topology (dict): The network topology.
        AS (str): The AS identifier.
    """
    # Generate the addresses dictionary
    
    with open("subnets.json") as json_file:
        addresses_dict = json.load(json_file)
        # Find the line to insert BGP configuration
        index_line = find_index(routeur, "ip forward-protocol nd\n") - 1
        # Insert BGP configuration
        insert_line(routeur, index_line,
                    f"router bgp 10{AS[-1]}\n"
                    f" bgp router-id {give_ID(routeur)}\n"
                    f" bgp log-neighbor-changes\n"
                    f" no bgp default ipv4-unicast\n")
        index_line += 4
        # Add neighbors for all routers in the same AS
        for router_in_as in topology[AS]['routers']:
            if router_in_as != routeur:
                neighbor_loopback = f"2001::{router_in_as[1:]}"
                insert_line(routeur, index_line, f" neighbor {neighbor_loopback} remote-as 10{AS[-1]}\n")
                insert_line(routeur, index_line + 1, f" neighbor {neighbor_loopback} update-source Loopback0\n")
                index_line += 2
        # Add neighbors for BGP for border routers
        for neighbor_info in addresses_dict[routeur]:
            for neighbor, details in neighbor_info.items():
                interface, ipv6_address, neighbor_AS = details
                if AS != neighbor_AS:
                    # Use the link address between the two routers
                    link_address = ipv6_address.split("::")[0] + "::" + ("2" if ipv6_address.endswith("::1/64") else "1")
                    insert_line(routeur, index_line, f" neighbor {link_address} remote-as 10{neighbor_AS[-1]}\n")
                    index_line += 1
        # Add address-family for IPv6
        insert_line(routeur, index_line, " address-family ipv4\n exit-address-family\n address-family ipv6\n  network 2001::/128\n")
        index_line += 4
        # Add network statements and activate neighbors in address-family
        for neighbor_info in addresses_dict[routeur]:
            for neighbor, details in neighbor_info.items():
                interface, ipv6_address, neighbor_AS = details
                # Format the network address
                network_address = ipv6_address.split("::")[0] + "::/64"
                insert_line(routeur, index_line, f"  network {network_address}\n")
                index_line += 1
                if AS == neighbor_AS:
                    # Use the Loopback address of the neighbor
                    neighbor_loopback = f"2001::{neighbor[1:]}"
                    insert_line(routeur, index_line, f"  neighbor {neighbor_loopback} activate\n")
                    index_line += 1
                else:
                    # Use the link address between the two routers
                    link_address = ipv6_address.split("::")[0] + "::" + ("2" if ipv6_address.endswith("::1/64") else "1")
                    insert_line(routeur, index_line, f"  neighbor {link_address} activate\n")
                    index_line += 1
        # Activate neighbors in address-family for all routers in the same AS
        for router_in_as in topology[AS]['routers']:
            if router_in_as != routeur:
                neighbor_loopback = f"2001::{router_in_as[1:]}"
                insert_line(routeur, index_line, f"  neighbor {neighbor_loopback} activate\n")
                index_line += 1
        insert_line(routeur, index_line, " exit-address-family\n")