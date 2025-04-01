import json
import time

from router import Router

def main(topology) :
    for AS in topology :
        for router in topology[AS]['routers'] :
            # Create a Router object for each router in the topology
            router_obj = Router(router, topology[AS]['routers'][router], topology[AS]['subnets'])
            # Generate the configuration file for the router
            config = router_obj.generate_routing_file()
            # Write the configuration to a file
            with open(f"{router}.cfg", "w") as file:
                file.write(config)
            # Print the configuration to the console 
            print(config)

if __name__ == "__main__":
    with open("intends.json", "r") as file:
        # Load topology from JSON file
        topology = json.load(file)
    start = time.time()
    main(topology)
    end = time.time()
    print("Total execution time:", end - start)

# Execute move_files with the correct path
