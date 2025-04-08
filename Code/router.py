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
        self.loopback += f" ip address {self.subnets[self.router_name]["loopback"][:-2]} {get_subnet(self.subnets[self.router_name]['loopback'])}\n"

        self.interfaces = {}
        for interface, specs in self.subnets[self.router_name].items():
            if interface != "ospf_cost" :
                if interface != "loopback":
                    self.interfaces[interface] = f" interface {interface}\n"
                    self.interfaces[interface] += f" ip address {get_subnet(specs['ip'])} {get_mask(specs['ip'])}\n"
                    if interface == "FastEthernet0/0" : self.interfaces[interface] += " duplex full\n"
                    self.interfaces[interface] += " negociate auto\n"
                    
    def generate_ospf(self):
        """
        Génère la configuration du protocole de routage IGP (OSPF).

        Cette méthode est à utiliser pour les sous-classes : P et PE
        """
        self.max_path = 4
        self.file += "router ospf 1\n"

        for interface in self.subnets[self.router_name].keys():
            if interface == "loopback":
                self.file += " network {} {} area 0\n".format(
                    get_subnet(self.subnets[self.router_name]["loopback"]),
                    get_reversed_mask(self.subnets[self.router_name]["loopback"])
                )
            else: 
                self.file += " network {} {} area 0\n".format(
                    get_subnet(self.subnets[self.router_name][interface]["ip"]),
                    get_reversed_mask(self.subnets[self.router_name][interface]["ip"])
                )
        ### @todo: faut rajouter ça ou pas ?
        self.file += f" maximum-paths {self.max_path}\n"


    ### TODO il faut supprimer cette méthode car uniquement sur PE 
    def generate_bgp(self):
        """
        Génère la configuration du protocole de routage BGP.

        Cette méthode configure BGP pour le routeur, en définissant les voisins,
        leurs AS (Autonomous System) et les sources de mise à jour.

        Pour chaque interface non-loopback :
        - Configure l'AS distant.
        - Définit la source de mise à jour comme Loopback0.
        """
        interface = self.subnets[self.router_name].keys()[0]
        self.file += f"router bgp {self.subnets[self.router_name][interface]['AS_number']}\n"
        self.file += f" bgp router-id {self.subnets[self.router_name]['loopback']}\n"
        self.file += " bgp log-neighbor-changes\n"
        
        
        ### différences entre PE et CE : PE a des liens BGP dans le backbone et advertise en loopback : 
        ### PE : neighbor {loopback} remote-as 65000
        ### CE : neighbor {ip} remote-as 65001  
        ### self.bgp_neighbors = [ router for router in self.intent[self.router_name].keys() if router != "loopback" ]
        

    def generate_finale_config(self):
        """
        Ajoute la configuration finale au fichier de configuration.

        Cette méthode complète le fichier de configuration avec les paramètres
        finaux nécessaires pour le routeur.
        """
        self.file += FINAL_CONFIG

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
