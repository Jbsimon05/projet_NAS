from router import Router
from template import *
from tools import insert_line, find_index, get_mask, get_subnet, get_reversed_mask

class CE(Router):
    """
    Customer Edge (CE) router.
    """
    def __init__(self, router_name, intent, subnets):
        super().__init__(router_name, intent, subnets)

    def generate_interfaces(self):
        super().generate_interfaces()
        self.file += self.loopback
        for interface in self.interfaces:
            self.file += "!\n" + interface + "!\n"
