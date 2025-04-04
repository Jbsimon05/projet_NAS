from template import *
from tools import insert_line, find_index, get_mask, get_subnet, get_reversed_mask

class Router:
    """
    Classe pour générer un routeur générique.
    """
    def __init__(self, router_name: str, intent: dict, subnets: dict):
        """
        Initialise un objet Router.

        Args:
            router_name (str): Nom du routeur.
            intent (dict): Intentions de configuration pour le routeur.
            subnets (dict): Dictionnaire contenant les sous-réseaux associés au routeur.
        """
        self.file = ""
        self.router_name = router_name
        self.intent = intent
        self.subnets = subnets

    def generate_init_config(self):
        """
        Génère la configuration initiale du routeur.

        Cette méthode ajoute les paramètres de base nécessaires pour initialiser
        la configuration du routeur.
        """
        self.file += INIT_CONFIG(self.router_name)
        self.file += "!\n"

    def generate_interfaces(self):
        """
        Génère la configuration des interfaces pour le routeur.

        Cette méthode configure les interfaces en fonction des sous-réseaux définis
        dans le dictionnaire `subnets`. Elle gère les interfaces de type loopback,
        FastEthernet et les liens OSPF ou IBGP.

        Pour chaque interface :
        - Configure l'adresse IP et le masque.
        - Ajoute des paramètres spécifiques comme OSPF, MPLS ou duplex.
        """
        
        self.loopback = f"interface loopback0\n"
        self.loopback += self.subnets[self.router_name]["loopback"]
        self.loopback += f" ip address {self.loopback} {get_subnet(self.loopback)}\n"

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
        """
        Génère la configuration du protocole de routage IGP (OSPF).

        Cette méthode configure OSPF pour les interfaces du routeur, en définissant
        les réseaux et les masques inversés associés.
        """
        self.file += "router ospf 1\n"
        for interface in self.subnets[self.router_name].keys():
            if interface != "loopback":
                self.file += " network {} {} area 0\n".format(
                    get_subnet(self.subnets[self.router_name][interface]["ip"]),
                    get_reversed_mask(self.subnets[self.router_name][interface]["ip"])
                )

    def generate_bgp(self):
        """
        Génère la configuration du protocole de routage BGP.

        Cette méthode configure BGP pour le routeur, en définissant les voisins,
        leurs AS (Autonomous System) et les sources de mise à jour.

        Pour chaque interface non-loopback :
        - Configure l'AS distant.
        - Définit la source de mise à jour comme Loopback0.
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
        """
        Ajoute la configuration finale au fichier de configuration.

        Cette méthode complète le fichier de configuration avec les paramètres
        finaux nécessaires pour le routeur.
        """
        self.file += FINAL_CONFIG

    def generate_routing_file(self):
        """
        Génère le fichier de configuration complet pour le routeur.

        Cette méthode appelle les différentes étapes de génération de configuration
        (initiale, interfaces, IGP, BGP et finale) et retourne le fichier complet.

        Returns:
            str: Le fichier de configuration complet sous forme de chaîne de caractères.
        """
        self.generate_init_config()
        self.generate_interfaces()
        self.generate_igp()
        self.generate_bgp()
        self.generate_finale_config()
        return self.file
