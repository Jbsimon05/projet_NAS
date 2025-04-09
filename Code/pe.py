from router import Router
from template import *
from tools import *


class PE(Router):

    def __init__(self, router_name, intent, subnets):


        super().__init__(router_name, intent, subnets)

    def generate_routing_file(self) -> str:
        print("waka")
        self.generate_init_config()
        self.generate_vrf()
        self.generate_init_config2(True)
        self.generate_interfaces()
        self.generate_ospf()
        self.generate_bgp()
        self.generate_finale_config()
        return self.file
    """
    Classe représentant un routeur Provider Edge (PE).
    """




    def generate_bgp(self):
        self.file += "router bgp {}\n".format(
            self.intent["Backbone"]["AS_number"] # creer cette fonction
        )
        self.file += f' bgp router-id {extract_ip_address(self.subnets[self.router_name]["loopback"])}\n'
        self.file += " bgp log-neighbor-changes\n"

        for neighbors in self.intent["Backbone"]["routers"]:
            if neighbors != self.router_name:
                self.file += " neighbor {} remote-as {}\n".format(
                    extract_ip_address(self.subnets[neighbors]["loopback"]), #loopback
                    self.intent["Backbone"]["AS_number"]
                )
                self.file += " neighbor {} update-source Loopback0\n".format(
                    extract_ip_address(self.subnets[neighbors]["loopback"]), #loopback
                )
        self.file += " !\n"
        self.file += " address-family ipv4\n"
        self.file += "  redistribute connected\n"
        for neighbors in self.intent["Backbone"]["routers"]:
            if neighbors != self.router_name:
                self.file += "  neighbor {} activate\n".format(
                    extract_ip_address(self.subnets[neighbors]["loopback"]), #loopback
                )
                self.file += "  neighbor {} send-community both\n".format(
                    extract_ip_address(self.subnets[neighbors]["loopback"]), #loopback
                )
        self.file += " exit-address-family\n"
        self.file += " !\n"
        self.file += " address-family vpnv4\n"	
        for neighbors in self.intent["Backbone"]["routers"]:
            if neighbors != self.router_name:
                self.file += "  neighbor {} activate\n".format(
                    extract_ip_address(self.subnets[neighbors]["loopback"]), #loopback
                )
                self.file += "  neighbor {} send-community both\n".format(
                    extract_ip_address(self.subnets[neighbors]["loopback"]), #loopback
                )
        self.file += " exit-address-family\n"
        self.file += " !\n"
  


                

        for neighbors in self.intent["Backbone"]["routers"][self.router_name]:

                if neighbors[0] == "C":
                    for keys in list(self.subnets[neighbors].keys()):
                        if keys[0][0] in "GF":
                            
                            ip = 0
                            for interface in self.subnets[neighbors]:
                                if interface != "loopback":
                                    if self.subnets[neighbors][interface]["neighbor"] == self.router_name:
                                        ip = self.subnets[neighbors][interface]["ip"]
                                        break

                            self.file += " address-family ipv4 vrf {}\n".format(
                                self.subnets[neighbors][keys]["vrf_name"] # creer cette fonction
                            )
                            self.file += "  neighbor {} remote-as {}\n".format(
                                extract_ip_address(ip), #loopback
                                self.subnets[neighbors][keys]["AS_number"] # creer cette fonction
                            )
                            self.file += "  neighbor {} activate\n".format(
                                extract_ip_address(ip), #loopback
                            )
                            self.file += "  neighbor {} send-community both\n".format(
                                extract_ip_address(ip), #loopback

                            )
                            self.file += " exit-address-family\n"

                            break










    
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
        
        self.file += f"interface loopback0\n"
        self.file += f" ip address {extract_ip_address(self.subnets[self.router_name]['loopback'])} {get_subnet_mask(self.subnets[self.router_name]['loopback'])}\n"

        self.interfaces = {}
        for interface, specs in self.subnets[self.router_name].items():
            if interface != "ospf_cost" :
                if interface != "loopback":
                    self.file += f"interface {interface}\n"
                    if self.subnets[self.router_name][interface]["linkType"] == "BGP":
                        neighbor = self.subnets[self.router_name][interface]["neighbor"]
                        for keys in list(self.subnets[neighbor].keys()):
                            if keys[0] in "GF": 
                                self.file += f' ip vrf forwarding {self.subnets[neighbor][keys]["vrf_name"]}\n'
                                break
                    self.file += f" ip address {extract_ip_address(specs['ip'])} {get_subnet_mask(specs['ip'])}\n"
                    if interface == "FastEthernet0/0" : self.file += " duplex full\n"
                    else : self.file += " negotiation auto\n"
                    if self.subnets[self.router_name][interface]["linkType"] == "OSPF":
                        self.file += " mpls ip\n"




    def generate_vrf(self):
        for CE in self.intent["Backbone"]["routers"][self.router_name]:
            if (CE[0] == "C") and (CE[1] == "E"):
                for keys in list(self.subnets[CE].keys()):
                    if keys[0][0] in "GF":
                        for keys2 in list(self.subnets[self.router_name].keys()):
                            if keys2[0][0] in "GF":

                                self.file += "ip vrf {}\n".format(
                                    self.subnets[CE][keys]["vrf_name"] # creer cette fonction
                                )
                            
                                self.file += " rd {}:{}\n".format(
                                    self.subnets[self.router_name][keys2]["AS_number"],
                                    self.subnets[CE][keys]["AS_number"] # creer cette fonction
                                )
                                self.file += " route-target export {}:{}\n".format(
                                    self.subnets[self.router_name][keys2]["AS_number"],
                                    self.subnets[CE][keys]["AS_number"] # creer cette fonction
                                )
                                self.file += " route-target import {}:{}\n".format(
                                    self.subnets[self.router_name][keys2]["AS_number"],
                                    self.subnets[CE][keys]["AS_number"] # creer cette fonction
                                )
                                self.file += "!\n"
                            
                                break
                        break




        




