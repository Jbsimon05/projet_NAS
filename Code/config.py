import os
from template import *

class ConfigGen:
    """
    Classe ConfigGenerator pour générer des fichiers de configuration de routeurs.
    Permet de créer des fichiers de configuration de base, d'insérer des lignes spécifiques,
    de trouver des indices de lignes et de générer des templates de configuration MPLS.
    """

    def __init__(self, router_name: str, config_num: int) -> None:
        """
        Initialise le générateur de configuration avec une configuration de base et un identifiant de routeur.
        Args:
            base_config (list): Les lignes de configuration de base.
            router (str): L'identifiant du routeur.
        """
        self.router_name = router_name
        self.filename = f"i{config_num}_startup-config.cfg"
