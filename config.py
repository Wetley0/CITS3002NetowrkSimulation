# Host A
HOST_A_NAME = "Host A"
HOST_A_IP = "10.0.1.10"
HOST_A_MAC = "AA:AA:AA:AA:AA:AA"
# The first route is not necessary at all but keep it for now
HOST_A_ROUTING_TABLE = {"10.0.1": ("", "10.0.1.10"),"default": ("", "10.0.1.1")}
HOST_A_MAC_TABLE = {"10.0.1.1": "BB:BB:BB:BB:BB:BB"}

# Host B
HOST_B_NAME = "Host B"
HOST_B_IP = "10.0.2.20"
HOST_B_MAC = "DD:DD:DD:DD:DD:DD"
# The first route is not necessary at all but keep it for now
HOST_B_ROUTING_TABLE = {"10.0.2": ("", "10.0.2.20"), "default": ("", "10.0.2.1")}
HOST_B_MAC_TABLE = {"10.0.2.1": "CC:CC:CC:CC:CC:CC"}


# Router Interface 1
R1_INTERFACE = "Interface1"
R1_NAME = "Router R1"
R1_IP = "10.0.1.1"
R1_MAC = "BB:BB:BB:BB:BB:BB"


# Router Interface 2
R2_INTERFACE = "Interface2"
R2_NAME = "Router R2"
R2_IP = "10.0.2.1"
R2_MAC = "CC:CC:CC:CC:CC:CC"

# Router Routing Table (needs potential fixing to be scaleable)
R_ROUTING_TABLE = {"10.0.1": ("Interface1", "DIRECT"), "10.0.2": ("Interface2", "DIRECT")}

#Router MAC Table
R_MAC_TABLE = {"10.0.1.10": "AA:AA:AA:AA:AA:AA", "10.0.2.20": "DD:DD:DD:DD:DD:DD"}

