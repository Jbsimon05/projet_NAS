from template import *
from tools import *

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
        
    def generate_init_config2(self, isMpls: bool):
        self.file += INIT_CONFIG2(isMpls)
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
        self.loopback += f" ip address {extract_ip_address(self.subnets[self.router_name]['loopback'])} {get_subnet_mask(self.subnets[self.router_name]['loopback'])}\n"

        self.interfaces = {}
        for interface, specs in self.subnets[self.router_name].items():
            if interface != "ospf_cost" :
                if interface != "loopback":
                    self.interfaces[interface] = f"interface {interface}\n"
                    self.interfaces[interface] += f" ip address {extract_ip_address(specs['ip'])} {get_subnet_mask(specs['ip'])}\n"
                    if interface == "FastEthernet0/0" : self.interfaces[interface] += " duplex full\n"
                    else : self.interfaces[interface] += " negotiation auto\n"
                    #self.interfaces[interface] += f" ip ospf cost {specs['ospf_cost']}\n"


    def generate_ospf(self):
        """
        Génère la configuration du protocole de routage IGP (OSPF).

        Cette méthode est à utiliser pour les sous-classes : P et PE
        """
        self.max_path = 3
        self.file += "router ospf 1\n"

        for interface in self.subnets[self.router_name].keys():
            if interface != "loopback":
                if self.subnets[self.router_name][interface]["linkType"] == "OSPF":
                    self.file += " network {} {} area 0\n".format(
                        extract_ip_address(self.subnets[self.router_name]["loopback"]),
                        get_wildcard_mask(self.subnets[self.router_name]["loopback"])
                    )
                else: 
                    self.file += " network {} {} area 0\n".format(
                        extract_ip_address(self.subnets[self.router_name][interface]["ip"]),
                        get_wildcard_mask(self.subnets[self.router_name][interface]["ip"])
                    )


        self.file += f" maximum-paths {self.max_path}\n"



        

    def generate_finale_config(self, isMpls: bool = False):
        """
        Ajoute la configuration finale au fichier de configuration.

        Cette méthode complète le fichier de configuration avec les paramètres
        finaux nécessaires pour le routeur.
        """
        self.file += FINAL_CONFIG(isMpls)
        self.file += "!\n"


    ### TODO : a supprimer à terme 
    # def generate_routing_file(self):
    #     """
    #     Génère le fichier de configuration complet pour le routeur.

    #     Cette méthode appelle les différentes étapes de génération de configuration
    #     (initiale, interfaces, IGP, BGP et finale) et retourne le fichier complet.

    #     Returns:
    #         str: Le fichier de configuration complet sous forme de chaîne de caractères.
    #     """
    #     self.generate_init_config()
    #     self.generate_interfaces()
    #     self.generate_bgp()
    #     self.generate_finale_config()
    #     return self.file
