from tools import *

class Router:
    def __init__(self, intent:dict):
        """
        content = contenu du fichier de configuration
        """
        self.content = ""
        self.intent = intent

    def generate_base(self):
        ...