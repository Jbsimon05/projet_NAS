import json

class SubnetsGen:

      def __init__(self, intent: dict):
            self.intent = intent
            self.subnet_dict = {}
            self.subnet_interconnexion_dict = {}
            self.router_neighbors = {}
            
            self.generate_addresses_dict()
            self.save_to_json()
            
            

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
            for AS in self.intent :
                  self.subnet_dict[AS] = {}
                  subnet_number = 1
                  # Iterate over each router of the current AS
                  for router in self.intent[AS]['routers'] :
                        # Iterate over each neighbor of the current router
                        for neighbor in self.intent[AS]['routers'][router] :
                              # To avoid duplicates, ensure the router with the smaller numeric suffix comes first
                              if router[1:] < neighbor[1:] :
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

      def give_subnet_interconnexion(self) -> None:
          """
          Generates a dict of subnets for the inter-AS connections.
          Args:
              self.intent (dict): The network self.intent.
              subnet_dict (dict): The subnet dictionary.
          Returns:
              dict: A dictionary of subnets for inter-AS connections.
          """
          # Create necessary dict
          last_entries = self.last_entries_subnet(self.subnet_dict)
          for AS in self.intent:
              self.subnet_interconnexion_dict[AS] = dict()
          # Iterate over each AS
          for AS in self.intent:
              # Iterate over each AS neighbor
              for AS_neighbor in self.intent[AS]['neighbor']:
                  # Iterate over each border Router
                  for router1 in self.intent[AS]['neighbor'][AS_neighbor]:
                      # Iterate over each neighbor Router
                      for router2 in self.intent[AS]['neighbor'][AS_neighbor][router1]:
                          # Check externality of the link
                          if (router1, router2) not in self.subnet_interconnexion_dict[AS].keys() and (router2, router1) not in self.subnet_interconnexion_dict[AS].keys():
                              # Create the end of the address of each externnal interface of borderRouters (ex. 111::1 -> AS 1, link 11, router 1)
                              if AS < AS_neighbor:
                                  self.subnet_interconnexion_dict[AS][(router1, router2)] = str(int(AS[3:])) + str((last_entries[AS] + 1)) + "::1"
                                  self.subnet_interconnexion_dict[AS_neighbor][(router2, router1)] = str(int(AS[3:])) + str((last_entries[AS] + 1)) + "::2"
                              else:
                                  self.subnet_interconnexion_dict[AS][(router1, router2)] = str(int(AS_neighbor[3:])) + str((last_entries[AS] + 1)) + "::1"
                                  self.subnet_interconnexion_dict[AS_neighbor][(router2, router1)] = str(int(AS_neighbor[3:])) + str((last_entries[AS] + 1)) + "::2"
                              last_entries[AS] += 1

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
          self.give_subnet_interconnexion()
          # Iterate over each AS
          for AS in self.intent:
              # Iterate over each router in the current AS
              for router in self.intent[AS]['routers']:
                  if router not in self.router_neighbors:
                      self.router_neighbors[router] = []
                  # Iterate over each neighbor of the current router
                  for neighbor, interface in self.intent[AS]['routers'][router].items():
                      # To ensure it's in the correct order
                      if router[1:] < neighbor[1:]:
                          subnet_index = self.subnet_dict[AS][(router, neighbor)]
                          router_index = 1
                      else:
                          subnet_index = self.subnet_dict[AS][(neighbor, router)]
                          router_index = 2
                      ipv6_address = f"{self.intent[AS]['address']}{subnet_index}::{router_index}{self.intent[AS]['subnet_mask']}"
                      self.router_neighbors[router].append({neighbor: [interface, ipv6_address, AS]})
          # Handle inter-AS connections
          for AS in self.intent:
              for AS_neighbor in self.intent[AS]['neighbor']:
                  for router1 in self.intent[AS]['neighbor'][AS_neighbor]:
                      for router2, interface in self.intent[AS]['neighbor'][AS_neighbor][router1].items():
                          if router1 not in self.router_neighbors:
                              self.router_neighbors[router1] = []
                          if router2 not in self.router_neighbors:
                              self.router_neighbors[router2] = []

                          # Check if the connection already exists to avoid duplication
                          if not any(neighbor.get(router2) for neighbor in self.router_neighbors[router1]):
                              if int(AS[3:]) < int(AS_neighbor[3:]):
                                  ipv6_address1 = f"{self.intent[AS]['address'][:-1]}{self.get_subnet_interconnexion(AS, router1, router2)}{self.intent[AS]['subnet_mask']}"
                                  ipv6_address2 = f"{self.intent[AS]['address'][:-1]}{self.get_subnet_interconnexion(AS_neighbor, router2, router1)}{self.intent[AS]['subnet_mask']}"
                              else:
                                  ipv6_address1 = f"{self.intent[AS]['address'][:-1]}{self.get_subnet_interconnexion(AS_neighbor, router2, router1)}{self.intent[AS]['subnet_mask']}"
                                  ipv6_address2 = f"{self.intent[AS]['address'][:-1]}{self.get_subnet_interconnexion(AS, router1, router2)}{self.intent[AS]['subnet_mask']}"

                              self.router_neighbors[router1].append({router2: [interface, ipv6_address1, AS_neighbor]})
                              self.router_neighbors[router2].append({router1: [interface, ipv6_address2, AS]})

      def save_to_json(self, filename: str = "subnets.json") -> None:
          """
          Save the router_neighbors configuration to a JSON file.
          Args:
              filename (str): The name of the JSON file. Defaults to 'subnets.json'.
          """
          with open(filename, "w") as json_file:
              json.dump(self.router_neighbors, json_file, indent=4)


sub = SubnetsGen("intends.json")