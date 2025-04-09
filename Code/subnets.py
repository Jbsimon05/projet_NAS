import json
import ipaddress
import ipaddress
from itertools import islice
from tools import add_ip

class SubnetsGen:
    """
    Classe pour générer des sous-réseaux et des interfaces pour un réseau donné à partir d'un fichier intends.json.
    """
    def __init__(self, intent: dict):
        """
        Initialise la classe avec l'intention réseau et génère les sous-réseaux et interfaces nécessaires.

        Args:
            intent (dict): Dictionnaire représentant l'intention réseau.
        """
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
        Génère un dictionnaire contenant les interfaces loopback pour chaque routeur du réseau.
        
        Exemple de sortie :
            {
                "R1": "192.168.1.1/32",
                "R2": "192.168.1.2/32",
                ...
            }
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
        Crée un dictionnaire associant un numéro unique à chaque lien physique du réseau.

        Returns:
            dict: Un dictionnaire avec des numéros uniques pour chaque lien physique.

        Exemple de sortie :
            {
                "AS_1": {
                    ("R1", "R2"): 1,
                    ("R1", "R3"): 2,
                    ...
                }
            }
        """
        self.subnet_dict = {}
        # Iterate over each AS
        subnet_number = 1
        for AS in self.intent:
            # Iterate over each router of the current AS
            for router in self.intent[AS]['routers']:
                # Iterate over each neighbor of the current router
                for neighbor in self.intent[AS]['routers'][router]:
                    # To avoid duplicates, ensure the router with the smaller numeric suffix comes first
                    if not (router, neighbor) in self.subnet_dict.keys() and not (neighbor, router) in self.subnet_dict.keys():
                        self.subnet_dict[(router, neighbor)] = subnet_number
                        subnet_number += 1

    def last_entries_subnet(self) -> None:
        """
        Trouve et retourne la dernière valeur de sous-réseau utilisée pour chaque AS.

        Returns:
            dict: Un dictionnaire contenant la dernière valeur de sous-réseau utilisée par AS.

        Exemple de sortie :
            {
                "AS_1": 5,
                "AS_2": 3,
                ...
            }
        """
        last_entry = dict()
        for AS in self.subnet_dict:
            last_entry[AS] = list(self.subnet_dict[AS].values())[-1]
        return last_entry

    def get_subnet_interconnexion(self, AS: str, routeur1: str, routeur2: str) -> str:
        """
        Récupère l'adresse IPv6 d'un sous-réseau d'interconnexion entre deux routeurs donnés.

        Args:
            AS (str): L'identifiant de l'AS.
            routeur1 (str): L'identifiant du premier routeur.
            routeur2 (str): L'identifiant du second routeur.

        Returns:
            str: L'adresse IPv6 du sous-réseau d'interconnexion.

        Exemple de sortie :
            "2001:db8::1/64"
        """
        return self.subnet_interconnexion_dict[AS][(routeur1, routeur2)] or self.subnet_interconnexion_dict[AS][(routeur2, routeur1)]

    def generate_all_subnets(self) -> None:
        self.all_subnets = list(islice(ipaddress.IPv4Network(self.intent["Backbone"]["address"]).subnets(new_prefix=29), 100))

    def generate_addresses_dict(self) -> None:
        """
        Génère un dictionnaire contenant les voisins, interfaces, adresses IP et AS pour chaque routeur.

        Returns:
            dict: Un dictionnaire avec les informations réseau pour chaque routeur.

        Exemple de sortie :
            {
                "R1": {
                    "GigabitEthernet1/0": {
                        "neighbor": "R2",
                        "ip": "2001:db8::1/64",
                        "AS": "AS_1",
                        "linkType": "OSPF"
                    },
                    ...
                },
                ...
            }
        """
        # Creates the subnet_dict
        self.give_subnet_dict()
        self.generate_all_subnets()
        print(self.subnet_dict)
        # Iterate over each AS
        for AS in self.intent:
            # Iterate over each router in the current AS
            for router in self.intent[AS]['routers']:
                if router not in self.subnets:
                    self.subnets[router] = {}
                # Iterate over each neighbor of the current router
                for neighbor, interface in {**self.intent[AS]['routers'][router], "loopback": "loopback"}.items():
                    if neighbor != "loopback":
                        # To ensure it's in the correct order
                        if self.subnet_dict.get((router, neighbor)):
                            subnet_index = self.subnet_dict[(router, neighbor)]
                            router_index = 1
                        elif self.subnet_dict.get((neighbor, router)):
                            subnet_index = self.subnet_dict[(neighbor, router)]
                            router_index = 2
                        ipv4_address = add_ip(self.all_subnets[subnet_index - 1], router_index)
                        self.subnets[router][interface["link"]] = {
                            "neighbor": neighbor, 
                            "ip" : ipv4_address, 
                            "AS_number": self.intent[AS]['AS_number'],
                            "vrf_name": AS,
                            "linkType": "BGP" if ( router[1] == "E" == neighbor[1] ) else "OSPF" 
                        }
                    else:
                        self.subnets[router][interface] = self.loopback_interfaces[router]
    def save_to_json(self, filename: str = "subnets.json") -> None:
        """
        Sauvegarde la configuration des sous-réseaux dans un fichier JSON.

        Args:
            filename (str): Le nom du fichier JSON. Par défaut 'subnets.json'.
        """
        with open(filename, "w") as json_file:
            json.dump(self.subnets, json_file, indent=4)


def main():
    """
    Fonction principale pour générer les sous-réseaux à partir d'un fichier intends.json.
    """
    # Load the intent from intends.json
    intent_file = "intent.json"
    with open(intent_file, "r") as file:
        intent = json.load(file)

    # Generate subnets.json using SubnetsGen
    subnets_gen = SubnetsGen(intent)
    subnets = subnets_gen.subnets  # Dictionary with subnets information

    # Save the configuration to a .json file
    config_filename = "subnets.json"
    with open(config_filename, "w") as config_file:
        json.dump(subnets, config_file, indent=4)

if __name__ == "__main__":
    main()
