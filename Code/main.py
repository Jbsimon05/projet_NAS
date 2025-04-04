import json
import time
from subnets import SubnetsGen, get_intent
from router import Router

def main():
    """
    Fonction principale pour générer les fichiers de configuration des routeurs.

    Étapes :
        1. Charger l'intention réseau depuis le fichier `intends.json`.
        2. Générer les sous-réseaux à partir de l'intention et les sauvegarder dans un dictionnaire.
        3. Créer les fichiers de configuration pour chaque routeur en fonction des sous-réseaux générés.
        4. Sauvegarder chaque configuration dans un fichier `.cfg` correspondant au routeur.

    """
    # Charger intends.json
    intent_file = "intends.json"
    intent = get_intent(intent_file)

    # Générer subnets.json à l'aide de SubnetsGen
    subnets_gen = SubnetsGen(intent)
    subnets = subnets_gen.subnets  # Dictionnaire contenant les informations des sous-réseaux

    # Générer les fichiers de configuration pour chaque routeur
    for router_name in subnets:
        router = Router(router_name, intent, subnets)
        config = router.generate_routing_file()

        # Sauvegarder la configuration dans un fichier .cfg
        config_filename = f"{router_name}.cfg"
        with open("../testConfigFiles/" + config_filename, "w") as config_file:
            config_file.write(config)

if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print("Temps d'exécution total :", end - start)
