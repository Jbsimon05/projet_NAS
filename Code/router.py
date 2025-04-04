from template import *
from tools import insert_line, find_index, get_mask, get_subnet, get_reversed_mask

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
            self.file += f"interface {interface}\n"
            if interface == "loopback":
                ip = get_subnet(specs)
                mask = get_mask(specs)
                self.file += f" ip address {ip} {mask}\n"
                if self.router_name[0] == "P":
                    self.file += " ip ospf 1 area 0\n"
            else:
                ip = get_subnet(specs["ip"])
                mask = get_mask(specs["ip"])
                self.file += f" ip address {ip} {mask}\n"
                if interface == "FastEthernet0/0" : self.file += "duplex full\n"
                if self.specs["linkType"] == "OSPF" : self.file += " ip ospf 1 area 0\n"
                self.file += " mpls ip\n"
            self.file += "!\n"

    def generate_igp(self):
        self.file += "router ospf 1\n"

        for interface in self.subnets[self.router_name].keys():
            if interface != "loopback":
                self.file += " network {} {} area 0\n".format(
                    get_subnet(self.subnets[self.router_name][interface]["ip"]),
                    get_reversed_mask(self.subnets[self.router_name][interface]["ip"])
                )

    def generate_finale_config(self):
        self.file += FINAL_CONFIG

    def generate_routing_file(self):
        self.generate_init_config()

        self.generate_interfaces()
        self.generate_igp()

        self.generate_finale_config()
        
        return self.file
