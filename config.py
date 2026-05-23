# Host A
HOST_A_NAME = "Host A"
HOST_A_IP = "10.0.1.10"
HOST_A_MAC = "AA:AA:AA:AA:AA:AA"
# The first route is not necessary at all but keep it for now
HOST_A_ROUTING_TABLE = {"default": "10.0.1.1"}
HOST_A_MAC_TABLE = {"10.0.1.1": "BB:BB:BB:BB:BB:BB"}

# Host B
HOST_B_NAME = "Host B"
HOST_B_IP = "10.0.2.20"
HOST_B_MAC = "DD:DD:DD:DD:DD:DD"
# The first route is not necessary at all but keep it for now
HOST_B_ROUTING_TABLE = {"default": "10.0.2.1"}
HOST_B_MAC_TABLE = {"10.0.2.1": "CC:CC:CC:CC:CC:CC"}


# Router
R1_NAME = "Router R1"

# Router Interface 1
R1_INTERFACE1 = "Interface 1"
R1_IP1 = "10.0.1.1"
R1_MAC1 = "BB:BB:BB:BB:BB:BB"


# Router Interface 2
R1_INTERFACE2 = "Interface 2"
R1_IP2 = "10.0.2.1"
R1_MAC2 = "CC:CC:CC:CC:CC:CC"

# Router Routing Table (needs potential fixing to be scaleable)
R1_ROUTING_TABLE = {"10.0.1": ("Interface 1", "DIRECT"), "10.0.2": ("Interface 2", "DIRECT")}

#Router MAC Table
R1_MAC_TABLE = {"10.0.1.10": "AA:AA:AA:AA:AA:AA", "10.0.2.20": "DD:DD:DD:DD:DD:DD"}

