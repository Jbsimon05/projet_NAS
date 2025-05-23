INIT_CONFIG = lambda router_name : f"""\
enable
version 15.2
service timestamps debug datetime msec
service timestamps log datetime msec
hostname {router_name}
boot-start-marker
boot-end-marker
no aaa new-model
no ip icmp rate-limit unreachable
ip cef
"""

INIT_CONFIG2 = lambda isMpls : f"""\
no ip domain lookup
mpls label protocol ldp
no ipv6 cef
{"multilink bundle-name authenticated" if isMpls else "!"}
ip tcp synwait-time 5"""

FINAL_CONFIG = lambda isMpls : f"""\
ip forward-protocol nd
no ip http server
no ip http secure-server
control-plane
line con 0
 exec-timeout 0 0
{"mpls ip" if isMpls else "!"}
 privilege level 15
 logging synchronous
 stopbits 1
line aux 0
 exec-timeout 0 0
 privilege level 15
 logging synchronous
 stopbits 1
line vty 0 4
 login
end
"""
