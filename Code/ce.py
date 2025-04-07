from router import Router
from tools import get_subnet, get_mask, get_reversed_mask

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
        self.generate_interfaces()
        self.generate_bgp()
        self.generate_finale_config()
        return self.file

    def generate_interfaces(self):
        """
        Génère la configuration des interfaces pour le routeur CE.
        """
        self.file += f"interface Loopback0\n"
        self.file += f" ip address {self.subnets[self.router_name]['loopback']}\n!\n"

        for interface, specs in self.subnets[self.router_name].items():
            if interface != "loopback":
                self.file += f"interface {interface}\n"
                self.file += f" ip address {specs['ip']} {get_mask(specs['ip'])}\n"
                if "FastEthernet" in interface:
                    self.file += " duplex full\n"
                self.file += " negotiation auto\n!\n"

    def generate_bgp(self):
        """
        Génère la configuration BGP pour le routeur CE.
        """
        as_number = self.subnets[self.router_name]["FastEthernet0/0"]["AS_number"]
        neighbor_ip = self.subnets[self.router_name]["FastEthernet0/0"]["ip"]

        self.file += f"router bgp {as_number}\n"
        self.file += f" bgp router-id {self.subnets[self.router_name]['loopback']}\n"
        self.file += " bgp log-neighbor-changes\n"
        self.file += f" neighbor {neighbor_ip} remote-as {as_number}\n"
        self.file += " !\n"
        self.file += " address-family ipv4\n"
        self.file += "  redistribute connected\n"
        self.file += f"  neighbor {neighbor_ip} activate\n"
        self.file += f"  neighbor {neighbor_ip} allowas-in 2\n"
        self.file += " exit-address-family\n"
