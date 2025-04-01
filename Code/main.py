import json
import time

from config import create_base_cfg
from protocols import activate_protocols
from router import Router
from subnets import SubnetsGen


def main(topology) :
    """
    Main function to configure routers based on the given topology.
    Args:
        topology (dict): The network topology.
    """
    for AS in topology :
        for router in topology[AS]['routers'] :
            # Create a blank config file
            create_base_cfg(base_config, router)
            # Configure Loopback0 interface
            create_loopback_interface(router)
            # Configure IPv6 addressing
            create_interfaces(router, topology, AS)
            # Activate RIP, OSPF, and BGP protocols
            activate_protocols(AS, router, topology)


if __name__ == "__main__":
    with open("intends.json", "r") as file:
        # Load topology from JSON file
        topology = json.load(file)
    start = time.time()
    main(topology)
    end = time.time()
    print("Total execution time:", end - start)

# Execute move_files with the correct path
