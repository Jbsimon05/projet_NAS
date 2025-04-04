import json
import ipaddress

class SubnetsGen:

    def __init__(self, intent: dict):
        self.intent = intent
        self.subnet_dict = {}
        self.subnets = {}
        self.loopback_interfaces = {}
        
        self.get_loopback_interfaces()
        self.generate_addresses_dict()
        
        # peut être mis en commentaire 
        self.save_to_json()
        
    def get_loopback_interfaces(self) -> None:
        """
        Generates a dictionary with loopback interfaces for each router in the network.
        """
        loopbackref = self.intent["Backbone"]["loopback"]
        # Iterate over each AS
        count = 0
        for AS in self.intent:
            # Skip non-AS keys
            # Iterate over each router in the current AS
            for router in self.intent[AS]['routers'].keys():
                count += 1
                ip = ipaddress.ip_network(loopbackref).network_address + count
                self.loopback_interfaces[router] = f"{ip}/32"

        
    def give_subnet_dict(self) -> dict:
        """
        Creates a dict associating a unique number to every physical link in the network.
        Args:
        self.intent (dict): The network self.intent.
        Returns:
        dict: A dictionary with unique numbers for each physical link.
        Example:
        {'AS_1': {('R1', 'R2'): 1, ('R1', 'R3'): 2, ... }}
        """
        self.subnet_dict = {}
        # Iterate over each AS
        for AS in self.intent:
            self.subnet_dict[AS] = {}
            subnet_number = 1
            # Iterate over each router of the current AS
            for router in self.intent[AS]['routers']:
                # Iterate over each neighbor of the current router
                for neighbor in self.intent[AS]['routers'][router]:
                    # To avoid duplicates, ensure the router with the smaller numeric suffix comes first
                    if router[1:] < neighbor[1:]:
                        self.subnet_dict[AS][(router, neighbor)] = subnet_number
                        subnet_number += 1

    def last_entries_subnet(self) -> None:
        """
        Find and return the last subnet value used.
        Args:
        subnet_dict (dict): The subnet dictionary.
        Returns:
        int: The last subnet value used.
        """
        last_entry = dict()
        for AS in self.subnet_dict:
            last_entry[AS] = list(self.subnet_dict[AS].values())[-1]
        return last_entry

    def get_subnet_interconnexion(self, AS: str, routeur1: str, routeur2: str) -> str:
        """
        Retrieve the IPv6 address of an interconnection subnet between two given routers.
        Args:
            AS (str): The AS identifier.
            subnet_interconnexion_dict (dict): The interconnection subnet dictionary.
            routeur1 (str): The first router identifier.
            routeur2 (str): The second router identifier.
        Returns:
            str: The IPv6 address of the interconnection subnet.
        """
        return self.subnet_interconnexion_dict[AS][(routeur1, routeur2)] or self.subnet_interconnexion_dict[AS][(routeur2, routeur1)]

    def generate_addresses_dict(self) -> None:
        """
        Generates a dictionary with neighbors, interfaces, IP addresses, and AS for each router.
        Args:
            self.intent (dict): The network self.intent.
        Returns:
            dict: A dictionary with neighbors, interfaces, IP addresses, and AS for each router.
        Output format:
            {
                "R1": [{"R2": ["GigabitEthernet1/0", "2001::1", "AS_1"]}, {"R3": ["interface", "ipv6 address", "AS"]}, ...],
                "R2": [{"R1": ["interface", "ipv6 address", "AS"]}, {"R4": ["interface", "ipv6 address", "AS"]}, ...],
                ...
            }
        """
        # Creates the subnet_dict
        self.give_subnet_dict()
        # Iterate over each AS
        for AS in self.intent:
            # Iterate over each router in the current AS
            for router in self.intent[AS]['routers']:
                if router not in self.subnets:
                    self.subnets[router] = {}
                # Iterate over each neighbor of the current router
                for neighbor, interface in {**self.intent[AS]['routers'][router], "abc": "loopback"}.items():
                    if neighbor != "abc":
                        # To ensure it's in the correct order
                        if router[1:] < neighbor[1:]:
                            subnet_index = self.subnet_dict[AS][(router, neighbor)]
                            router_index = 1
                        elif self.subnet_dict[AS].get((neighbor, router)):
                            subnet_index = self.subnet_dict[AS][(neighbor, router)]
                            router_index = 2
                        ipv6_address = f"{self.intent[AS]['address'][:-1]}{subnet_index}{self.intent[AS]['subnet_mask']}"
                        self.subnets[router][interface] = {
                            "neighbor": neighbor, 
                            "ip" : ipv6_address, 
                            "AS": AS,
                            "linkType": "OSPF" if router[0] == "P" == neighbor[0] else "IBGP"
                        }
                    else:
                        self.subnets[router][interface] = self.loopback_interfaces[router]

    def save_to_json(self, filename: str = "subnets.json") -> None:
        """
        Save the subnets configuration to a JSON file.
        Args:
            filename (str): The name of the JSON file. Defaults to 'subnets.json'.
        """
        with open(filename, "w") as json_file:
            json.dump(self.subnets, json_file, indent=4)

def get_intent(filename: str) -> dict:
    """
    Load the intent from a JSON file.
    Args:
        filename (str): The path to the JSON file.
    Returns:
        dict: The intent dictionary loaded from the file.
    Raises:
        FileNotFoundError: If the file does not exist.
    """
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"The file '{filename}' was not found. Please ensure the file exists in the correct path.")

intent_file = get_intent("intends.json")
sub = SubnetsGen(intent_file)


"""


{
    "PE1": {
        "Loopback0": "192.168.1.4/32",
        "FastEthernet0/0": {
            "neighbor": "P1",
            "IP": "192.168.1.4/8",
            "Area": "Backbone"
        }
    }
"}
"""