from router import Router
from template import *
from tools import insert_line, find_index, get_mask, get_subnet, get_reversed_mask


class P(Router):
    """
    Classe représentant un routeur Provider (P).
    """

    def __init__(self, router_name, intent, subnets):
        """
        Initialise un objet P.

        Args:
            router_name (str): Nom du routeur.
            intent (dict): Intentions de configuration pour le routeur.
            subnets (dict): Dictionnaire contenant les sous-réseaux associés au routeur.
        """
        super().__init__(router_name, intent, subnets)

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
        super().generate_interfaces()
        self.file += self.loopback
        for interface, config in self.interfaces.items():
            self.file += "!\n" + config
            if self.subnets[self.router_name][interface]["linkType"] == "OSPF":
                self.file += " mpls ip\n"

    def generate_routing_file(self):
        """
        Génère le fichier de configuration complet pour le routeur.

        Cette méthode appelle les différentes étapes de génération de configuration
        (initiale, interfaces, IGP, BGP et finale) et retourne le fichier complet.

        Returns:
            str: Le fichier de configuration complet sous forme de chaîne de caractères.
        """
        super().generate_init_config()
        super().generate_init_config2(True)
        self.generate_interfaces()
        super().generate_ospf()
        super().generate_finale_config()
        return self.file
