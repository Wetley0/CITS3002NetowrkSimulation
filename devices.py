from protocol import Transport, Network, Datalink
class Host:
    def __init__(self, name, routing_table, mac_table, ip, mac, network, mac_obj_table={}, port=8000):
        self.name = name
        self.ip = ip
        self.mac = mac
        self.network = network
        self.port = port
        self.mac_table = mac_table
        self.routing_table = routing_table
        self.seq = 0

        # For now maybe for good not sure but this will hold a dictionary of the objects connected to hosts
        self.mac_obj_table = mac_obj_table
        # If we can find a better method to bring in objects to the class to send data to then good

    def send_data(self, data, dest_ip, dest_port):
        payload_segment = Transport(self.port, dest_port, 0, data).encapsulate()
        packet = Network(self.ip, dest_ip, 17, 0, payload_segment).encapsulate()
        # print(packet)
        
        interface, next_hop = self.routing(packet)
        print(self.name, ": Layer 3: Packet forwarded to Data Link Layer")

        # Keep in mind for later I am passing the next hop and interface as parameters. (that do not go in init of datalink object) I do not know how you are meant to actually do so check this later when working
        # Also we may not need interface in the routing tables for hosts but now it is just a blank string maybe delete later
        dest_mac = self.mac_table_lookup(next_hop)
        frame = Datalink(self.mac, dest_mac, "0x0800", packet).encapsulate()
        router = self.mac_obj_table[dest_mac]
        router.receive_frame(frame, interface)
        return
    def receive_frame(self, frame, incoming_interface):
        print("frame recieved from router", frame, incoming_interface)
        return
    def handle_ack(self, ack_seq):
        return
    def attach_neighbour(self, ip, neighbour):
        self.neighbours[ip] = neighbour
    
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
    
    # Debugs will needed to be added to this later (like what is that ip address does not exist in mac_table so on)
    def mac_table_lookup(self, next_hop):
        return self.mac_table[next_hop]


class Router:
    def __init__(self, name, mac, routing_table, mac_table, mac_obj_table={}):
        self.name = name
        self.mac = mac
        self.routing_table = routing_table
        self.mac_table = mac_table
        self.mac_obj_table = mac_obj_table
    def receive_frame(self, frame, incoming_interface):
        print("frame received", frame, "With interface", incoming_interface)

        print("Not aware of interface yet still needs to be added")
        
        payload_packet = frame['payload_packet']
        self.process_packet(payload_packet)
        return
    
    def process_packet(self, packet):
        interface, next_hop = self.routing(packet)
        dest_mac = self.mac_table_lookup(next_hop)
        self.forward_packet(packet, interface, dest_mac)
        return 
    def routing(self, packet):
        dest_ip = packet['dest_ip']

        packet['ttl'] -= 1

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
    def forward_packet(self, packet, outgoing_interface, dest_mac):
        frame = Datalink(self.mac[outgoing_interface], dest_mac, "0x0800", packet).encapsulate()
        print("Router Next hop", dest_mac)

        host = self.mac_obj_table[dest_mac]
        host.receive_frame(frame, outgoing_interface)
        return
    def mac_table_lookup(self, next_hop):
        print("the next hop", next_hop)
        return self.mac_table[next_hop]
    def discover_interface(self, incoming_frame):
        return