from tools import *
from template import *

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


    def generate_interfaces(self):
        """
        Génère la configuration des interfaces pour le routeur.
        """
        ...
        
    def generate_igp(self):
        ...
        
    def generate_finale_config(self):
        self.file += FINAL_CONFIG

    def generate_routing_file(self):
        self.generate_init_config()

        self.generate_interfaces()
        self.generate_igp()

        self.generate_finale_config()
        
        return self.file