import json
import time
from subnets import SubnetsGen, get_intent
from router import Router

def main():
    # Load the intent from intends.json
    intent_file = "intends.json"
    intent = get_intent(intent_file)

    # Generate subnets.json using SubnetsGen
    subnets_gen = SubnetsGen(intent)
    subnets = subnets_gen.subnets  # Dictionary with subnets information

    # Generate configuration files for each router
    for router_name in subnets:
        router = Router(router_name, intent, subnets)
        config = router.generate_routing_file()

        # Save the configuration to a .cfg file
        config_filename = f"{router_name}.cfg"
        with open(config_filename, "w") as config_file:
            config_file.write(config)

if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print("Total execution time:", end - start)
