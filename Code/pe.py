from router import Router
from template import *
from tools import *


class PE(Router):

    def __init__(self, router_name, intent, subnets):


        super().__init__(router_name, intent, subnets)

    """
    Classe représentant un routeur Provider Edge (PE).
    """
    def generate_bgp(self):
        self.file += "router bgp {}\n".format(
            self.intent["Backbone"]["AS_number"] # creer cette fonction
        )
        self.file += f" bgp router-id {self.subnets[self.router_name]["loopback"]}\n"
        self.file += " bgp log-neighbor-changes\n"

        for neighbors in self.intent["Backbone"]["routers"]:
            if neighbors != self.router_name:
                self.file += " neighbor {} remote-as {}\n".format(
                    self.subnets[neighbors]["loopback"], #loopback
                    self.intent["Backbone"]["AS_number"]
                )
                self.file += " neighbor {} update-source Loopback0\n".format(
                    self.subnets[neighbors]["loopback"], #loopback
                )
        self.file += " !\n"
        self.file += " address-family ipv4\n"
        for neighbors in self.intent["Backbone"]["routers"]:
            if neighbors != self.router_name:
                self.file += "  neighbor {} activate\n".format(
                    self.subnets[neighbors]["loopback"], #loopback
                )
                self.file += "  neighbor {} send-community both\n".format(
                    self.subnets[neighbors]["loopback"], #loopback
                )
        self.file += " exit-address-family\n"
        self.file += " !\n"
        self.file += " address-family vpnv4\n"	
        for neighbors in self.intent["Backbone"]["routers"]:
            if neighbors != self.router_name:
                self.file += "  neighbor {} activate\n".format(
                    self.subnets[neighbors]["loopback"], #loopback
                )
                self.file += "  neighbor {} send-community both\n".format(
                    self.subnets[neighbors]["loopback"], #loopback
                )
        self.file += " exit-address-family\n"
        self.file += " !\n"
  


                

        for neighbors in self.intent["Backbone"]["routers"][self.router_name]:

                if neighbors[0] == "C":
                    for keys in list(self.subnets[neighbors].keys()):
                        if keys[0][0] in "GF":

                            self.file += " address-family ipv4 vrf {}\n".format(
                                self.subnets[neighbors][keys]["vrf_name"] # creer cette fonction
                            )
                            self.file += "  neighbor {} remote-as {}\n".format(
                                self.subnets[neighbors]["loopback"], #loopback
                                self.subnets[neighbors][keys]["AS_number"] # creer cette fonction
                            )
                            self.file += "  neighbor {} activate\n".format(
                                self.subnets[neighbors]["loopback"], #loopback
                            )
                            self.file += "  neighbor {} send-community both\n".format(
                                self.subnets[neighbors]["loopback"], #loopback

                            )
                            self.file += " exit address-family\n"

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
        super().generate_interfaces()
        self.file += self.loopback
        for interface, config in self.interfaces.items():
            if self.subnets[self.router_name][interface]["linkType"] == "BGP":
                neighbor = self.subnets[self.router_name][interface]["neighbor"]
                for keys in list(self.subnets[neighbor].keys()):
                    if keys[0][0] in "GF": 
                        self.file += f" ip vrf forwarding {self.subnets[neighbor][keys[0][0]]["vrf_name"]}\n"
                        break
            self.file += "!\n" + config
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




        

    def generate_routing_file(self) -> str:
        self.generate_init_config()
        self.generate_vrf()
        self.generate_init_config2(True)
        self.generate_interfaces()
        self.generate_ospf()
        self.generate_bgp()
        self.generate_finale_config()
        return self.file



