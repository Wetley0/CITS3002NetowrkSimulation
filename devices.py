from protocol import Transport, Network, Datalink
class Host:
    def __init__(self, name, routing_table, ip, mac, network, port=8000):
        self.name = name
        self.ip = ip
        self.mac = mac
        self.network = network
        self.port = port
        self.routing_table = routing_table
        self.seq = 0
    def send_data(self, data, dest_ip, dest_port, dest_mac):
        payload_segment = Transport(self.port, dest_port, 0, data).encapsulate()
        packet = Network(self.ip, dest_ip, 17, 0, payload_segment).encapsulate()
        # print(packet)
        
        interface, next_hop = self.routing(packet)
        print(self.name, ": Layer 3: Packet forwarded to Data Link Layer")

        # Keep in mind for later I am passing the next hop and interface as parameters. (that do not go in init of datalink object) I do not know how you are meant to actually do so check this later when working
        # Also we may not need interface in the routing tables for hosts but now it is just a blank string maybe delete later
        frame = Datalink(self.mac, dest_mac, "0x0800", packet)

        return
    def receive(self, frame):
        return
    def handle_ack(self, ack_seq):
        return
    
    # Routing is different fom host to router so the function will be within their respective classes
    def routing(self, packet):
        dest_ip = packet['dest_ip']

        print(self.name,": Layer 3: Destination IP read: ", dest_ip)
        print("HELLLLO", self.routing_table.items())
        for network, (interface, next_hop) in self.routing_table.items():
            if network != "default" and dest_ip.startswith(network):
                break
        else:
            interface, next_hop = self.routing_table["default"]

        print(self.name, ": Layer 3: Routing table lookup performed")
        print(self.name, ": Layer 3: Next-hop IP determined: ", next_hop)

        print(self.name, ": Layer 3: Outgoing interface selected ", interface)
        
        return interface, next_hop

class Router:
    def __init__(self, name, routing_table):
        self.name = name
        self.routing_table = routing_table
        self.mac_table = {}
    def receive_frame(self, frame, incoming_interface):
        return
    def process_packet(self, packet):
        return
    def forward_packet(self, packet, outgoing_interface, next_mac):
        return