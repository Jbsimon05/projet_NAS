from router import Router
from template import *
from tools import insert_line, find_index, get_mask, get_subnet, get_reversed_mask


class PE(Router):

    def __init__(self, router_name, intent, subnets, idrouter):


        super().__init__(router_name, intent, subnets)
        self.idrouter = idrouter
    """
    Classe représentant un routeur Provider Edge (PE).
    """
    def generate_bgp(self):
        self.file += "router bgp {}\n".format(
            self.intent["Backbone"]["AS_number"] # creer cette fonction
        )
        self.file += f" bgp router-id {self.idrouter}\n"
        self.file += " bgp log-neighbor-changes\n"

        for neighbors in self.intent["Backbone"]["routers"][self.router_name]:
            self.file += "neighbor {} remote-as {}\n".format(
                neighbors.idrouter, #loopback
                getAS() # creer cette fonction
            )
            self.file += "neighbor {} update-source Loopback0\n".format(
                get_id(PE) #loopback
            )
        self.file += " !\n"
        self.file += " address-family ipv4\n"
        for PE/P in ...:
            self.file += "  neighbor {} activate\n".format(
                get_id(PE) #loopback
            )
            self.file += "  neighbor {} send-community both\n".format(
                get_id(PE) #get loopback 
            )
        self.file += " exit-address-family\n"
        self.file += " !\n"
        for CE in ...:

            self.file += " address-family ipv4 vrf {}\n".format(
            get_vrf(CE) # creer cette fonction
            )
            self.file += "  neighbor {} remote-as {}\n".format(
                get_id(CE), #loopback
                get_as(CE) # creer cette fonction
            )
            self.file += "  neighbor {} activate\n".format(
                get_id(CE), #loopback

            )
            self.file += "  neighbor {} send-community both\n".format(
                get_id(CE), #loopback

            )
            self.file += " exit address-family\n"




    def generate_igp(self):
        self.file += "router ospf 1\n"
        for interface in self.subnets[self.router_name].keys():
            #if interface != "loopback":#
                self.file += " network {} {} area 0\n".format(
                    get_subnet(self.subnets[self.router_name][interface]["ip"]),
                    get_reversed_mask(self.subnets[self.router_name][interface]["ip"])
                )    
#a changer#
