import os
from template import *

class ConfigGenerator:
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

    def create_base_cfg(self) -> None:
        """
        Crée un fichier de configuration de base avec le nom d'hôte du routeur.
        Écrit les lignes de configuration de base et ajoute une ligne pour le nom d'hôte.
        """
        with open(self.filename, 'w') as file:
            for entry in self.base_config:
                file.write(entry + '\n')
        self.insert_line(3, f"hostname {self.router}\n")

    def insert_line(self, index_line: int, data: str) -> None:
        """
        Insère une ligne de données à un index spécifique dans le fichier de configuration.
        Args:
            index_line (int): L'index de la ligne où insérer les données.
        """
        with open(self.filename, 'r') as file:
            lines = file.readlines()
        lines.insert(index_line, data)
        with open(self.filename, 'w') as file:
            file.writelines(lines)

    def find_index(self, line: str) -> int:
        """
        Trouve l'index d'une ligne spécifique dans le fichier de configuration.
        Args:
            line (str): La ligne à rechercher dans le fichier de configuration.
        Returns:
            int: L'index de la ligne dans le fichier de configuration.
        """
        with open(self.filename, 'r') as file:
            lines = file.readlines()
        return lines.index(line)

    def generate_mpls_template(self) -> None:
        """
        Génère un template de configuration MPLS pour le routeur.
        Ajoute les lignes nécessaires pour activer le protocole MPLS.
        """
        self.create_base_cfg()
        self.insert_line(10, "mpls label protocol ldp\n")
        self.insert_line(20, "mpls ip\n")
        # debugging
        # print(f"Template de configuration MPLS généré pour {self.router} dans {self.filename}.")

if __name__ == "__main__":
    """
    Code de test pour la classe ConfigGenerator.
    Crée une instance de ConfigGenerator avec une configuration de base et un routeur donné.
    Génère un template de configuration MPLS pour le routeur spécifié.
    """
    base_config = [
        "version 15.2",
        "service timestamps debug datetime msec",
        "service timestamps log datetime msec",
        "boot-start-marker",
        "boot-end-marker",
        "no aaa new-model",
        "no ip icmp rate-limit unreachable",
        "ip cef",
        "no ip domain lookup",
        "no ipv6 cef",
        "multilink bundle-name authenticated",
        "ip tcp synwait-time 5",
        "ip forward-protocol nd",
        "no ip http server",
        "no ip http secure-server",
        "control-plane",
        "line con 0",
        " exec-timeout 0 0",
        " privilege level 15",
        " logging synchronous",
        " stopbits 1",
        "line aux 0",
        " exec-timeout 0 0",
        " privilege level 15",
        " logging synchronous",
        " stopbits 1",
        "line vty 0 4",
        " login",
        "end"
    ]
    router = "RouterName"
    generator = ConfigGenerator(base_config, router)
    generator.generate_mpls_template()
