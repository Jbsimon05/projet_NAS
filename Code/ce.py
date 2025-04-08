from router import Router
from tools import *

class CE(Router):
    """
    Classe pour générer un routeur CE (Customer Edge).
    Hérite de la classe Router.
    """
    def __init__(self, router_name: str, intent: dict, subnets: dict):
        super().__init__(router_name, intent, subnets)

    def generate_routing_file(self) -> str:
        """
        Génère le fichier de configuration complet pour un routeur CE.

        Returns:
            str: Le fichier de configuration complet sous forme de chaîne de caractères.
        """
        self.generate_init_config()
        self.generate_init_config2(False)
        self.generate_interfaces()
        self.generate_bgp()
        self.generate_finale_config()
        return self.file

    def generate_interfaces(self):
        """
        Génère la configuration des interfaces pour le routeur CE.
        """
        super().generate_interfaces()
        self.file += self.loopback
        for interface, config in self.interfaces.items():
            self.file += "!\n" + config
            if self.subnets[self.router_name][interface]["linkType"] == "OSPF":
                self.file += " mpls ip\n"
        self.file += f"interface Loopback0\n"
        self.file += f" ip address {self.subnets[self.router_name]['loopback']}\n!\n"

    def generate_bgp(self):
        """
        Génère la configuration BGP pour le routeur CE.
        """
        as_number = None
        for keys in list(self.subnets[self.router_name].keys()):
            if keys[0][0] in "GF": 
                as_number = self.subnets[self.router_name][keys]["AS_number"]
                break

        link = None
        neighbor = None
        for interface in self.subnets[self.router_name]:
            if interface != "loopback":
                if self.subnets[self.router_name][interface]["neighbor"][:2] == "PE":
                    neighbor = self.subnets[self.router_name][interface]["neighbor"]
                    link = interface

        neighbor_ip = self.subnets[neighbor][link]["ip"]

        self.file += f"router bgp {as_number}\n"
        self.file += f" bgp router-id {self.subnets[self.router_name]['loopback']}\n"
        self.file += " bgp log-neighbor-changes\n"
        self.file += f" neighbor {neighbor_ip} remote-as {as_number}\n"
        self.file += " !\n"
        self.file += " address-family ipv4\n"
        self.file += "  redistribute connected\n"
        self.file += f"  neighbor {extract_ip_address(neighbor_ip)} activate\n"
        self.file += f"  neighbor {extract_ip_address(neighbor_ip)} allowas-in 2\n"
        self.file += " exit-address-family\n"

