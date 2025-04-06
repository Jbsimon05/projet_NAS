from router import Router
from template import *
from tools import insert_line, find_index, get_mask, get_subnet, get_reversed_mask

class CE(Router):
    """
    Classe pour générer un Customer Edge (CE) router.
    """
    def __init__(self, router_name, intent, subnets):
        """
        Initialise un objet CE.

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
        for config in self.interfaces.values():
            self.file += "!\n" + config + "!\n"

    def generate_routing_file(self):
        """
        Génère le fichier de configuration complet pour le routeur.

        Cette méthode appelle les différentes étapes de génération de configuration
        (initiale, interfaces, IGP, BGP et finale) et retourne le fichier complet.

        Returns:
            str: Le fichier de configuration complet sous forme de chaîne de caractères.
        """
        super().generate_init_config()
        self.generate_interfaces()
        super().generate_finale_config()
        return self.file
