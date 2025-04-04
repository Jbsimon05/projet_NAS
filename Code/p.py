from router import Router
from template import *
from tools import insert_line, find_index, get_mask, get_subnet, get_reversed_mask


class P(Router):
    """
    Provider (P) router.
    """
    def generate_igp(self):
        self.file += "router ospf 1\n"
        for interface in self.subnets[self.router_name].keys():
            #if interface != "loopback":#
                self.file += " network {} {} area 0\n".format(
                    get_subnet(self.subnets[self.router_name][interface]["ip"]),
                    get_reversed_mask(self.subnets[self.router_name][interface]["ip"])
                )