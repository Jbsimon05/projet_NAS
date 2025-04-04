from router import Router
from template import *
from tools import insert_line, find_index, get_mask, get_subnet, get_reversed_mask


class C(Router):
    """
    Customer (C) router.
    """
    def generate_interfaces(self):
        """
        Override interface configuration for C routers.
        """
        super().generate_interfaces()
        self.file += " no ip domain-lookup\n"