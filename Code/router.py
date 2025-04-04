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
        
        self.file += f"interface loopback0\n"
        self.loopback = self.subnets[self.router_name]["loopback"]
        self.file += f" ip address {self.loopback} {get_subnet(self.loopback)}\n"

        self.interfaces = ["" for i in range(4)]
        i = 0
        for interface, specs in self.subnets[self.router_name].items():
            if interface != "loopback":
                self.interfaces[i] += f"interface {interface}\n"
                self.interfaces[i] += f" ip address {get_subnet(specs["ip"])} {get_mask(specs["ip"])}\n"
                if interface == "FastEthernet0/0" : self.interfaces[i] += "duplex full\n"
                self.interfaces[i] += "negociate auto\n"
            i += 1

    def generate_igp(self):
        self.file += "router ospf 1\n"
        for interface in self.subnets[self.router_name].keys():
            if interface != "loopback":
                self.file += " network {} {} area 0\n".format(
                    get_subnet(self.subnets[self.router_name][interface]["ip"]),
                    get_reversed_mask(self.subnets[self.router_name][interface]["ip"])
                )
    def generate_bgp(self):
        """
        Génère la configuration BGP pour le routeur.
        """
        self.file += "router bgp 10\n"
        self.file += f" bgp router-id {self.router_name}\n"
        self.file += " bgp log-neighbor-changes\n"
        self.file += " no bgp default ipv4-unicast\n"

        for interface, specs in self.subnets[self.router_name].items():
            if interface != "loopback":
                neighbor_ip = get_subnet(specs["ip"])
                neighbor_as = specs["AS"]
                self.file += f" neighbor {neighbor_ip} remote-as {neighbor_as}\n"
                self.file += f" neighbor {neighbor_ip} update-source Loopback0\n"

    def generate_finale_config(self):
        self.file += FINAL_CONFIG

    def generate_routing_file(self):
        self.generate_init_config()
        self.generate_interfaces()
        self.generate_igp()
        self.generate_bgp()
        self.generate_finale_config()
        return self.file
