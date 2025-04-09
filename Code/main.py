import json
import time
from pathlib import Path
from subnets import SubnetsGen
from router import Router
from c import C
from p import P
from pe import PE
from ce import CE
from tools import get_router_name

with open('intent.json', 'r') as file:
    data = json.load(file)

subnet = SubnetsGen(data)

with open('subnets.json', 'r') as file:
    subnets = json.load(file)

### @TODO : changer ce path
local_path = Path("/mnt/c/Users/pault/GNS3/projects/projet_NAS_final2/project-files/dynamips")

directories = []
for d in local_path.iterdir():
    if d.is_dir():
        directories.append(d)

def edit_config(directories: list[Path], data: dict, subnets: dict) -> None:
    for d in directories:
        dir = d / "configs/"
        for item in dir.iterdir():
            if item.name.startswith("i") and item.name.endswith("_startup-config.cfg"):
                with open(item, 'r') as file:
                    content = file.read()

                router_name = get_router_name(content)

                if router_name[:2] == "PE":
                    router = PE(router_name, data, subnets)
                elif router_name[:2] == "CE":
                    router = CE(router_name, data, subnets)
                elif router_name[0] == "P":
                    router = P(router_name, data, subnets)
                elif router_name[0] == "C":
                    router = C(router_name, data, subnets)
                    
                new_content = router.generate_routing_file()

                print("printed on file ", file.name[-22:])
                with open(item, 'w') as file:
                    file.write(new_content)

def edit_config_test(data: dict, subnets: dict):
    """
    Fonction principale pour générer les fichiers de configuration des routeurs.

    Étapes :
        1. Charger l'intention réseau depuis le fichier `intends.json`.
        2. Générer les sous-réseaux à partir de l'intention et les sauvegarder dans un dictionnaire.
        3. Créer les fichiers de configuration pour chaque routeur en fonction des sous-réseaux générés.
        4. Sauvegarder chaque configuration dans un fichier `.cfg` correspondant au routeur.

    """
    # Générer les fichiers de configuration pour chaque routeur
    for router_name in subnets:
        if router_name[:2] == "PE":
            router = PE(router_name, data, subnets)
        elif router_name[:2] == "CE":
            router = CE(router_name, data, subnets)
        elif router_name[0] == "P":
            router = P(router_name, data, subnets)
        elif router_name[0] == "C":
            router = C(router_name, data, subnets)
            
        new_content = router.generate_routing_file()

        config_filename = f"{router_name}.cfg"
        with open("../testConfigFiles/" + config_filename, "w") as config_file:
            config_file.write(new_content)

if __name__ == "__main__":
    start = time.time()
    edit_config(directories, data, subnets)
    edit_config_test(data, subnets)
    end = time.time()
    print("Temps d'exécution total :", end - start)
