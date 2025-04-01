from template import *
from tools import insert_line, find_index, get_subnet, get_reversed_mask, get_ip_and_mask

class Router:

    def __init__(self, router_name:str, intent:dict, subnets:dict):
        """
        content = contenu du fichier de configuration
        """
        self.file = ""
        self.router_name = router_name
        self.intent = intent
        self.subnets = subnets

    def generate_init_config(self):
        self.file += INIT_CONFIG(self.router_name)
        self.file += "!\n"

    def generate_interfaces(self):
        """
        Génère la configuration des interfaces pour le routeur.
        """
        for interface, specs in self.subnets[self.router_name].items():
            ip, mask = get_ip_and_mask(specs["IP"])
            self.file += f"interface {interface}\n"
            self.file += f" ip address {ip} {mask}\n"
            if "duplex" in specs:
                self.file += f" duplex {specs['duplex']}\n"
            if "mpls" in specs and specs["mpls"]:
                self.file += " mpls ip\n"
            self.file += "!\n"

    def generate_igp(self):
        self.file += "router ospf 1\n"

        for neighbor in self.subnets[self.router_name]:
            self.file += " network {} {} area 0\n".format(
                get_subnet(self.subnets[self.router_name][neighbor.keys()][1]),
                get_reversed_mask(self.subnets[self.router_name][neighbor.keys()][1])
            )

    def generate_finale_config(self):
        self.file += FINAL_CONFIG

    def generate_routing_file(self):
        self.generate_init_config()

        self.generate_interfaces()
        self.generate_igp()

        self.generate_finale_config()
        
        return self.file
