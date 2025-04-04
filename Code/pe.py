from router import Router
from template import *
from tools import insert_line, find_index, get_mask, get_subnet, get_reversed_mask


class PE(Router):
    """
    Provider Edge (PE) router.
    """
    def generate_bgp(self):
#a changer#