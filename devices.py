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


        # The ACK doesn't know the desired ip's, so we are storing it here for now
        self.dest_ip = 0;

        
        self.seq = 0
        self.expected_ack = 0

        # For now maybe for good not sure but this will hold a dictionary of the objects connected to hosts
        self.mac_obj_table = mac_obj_table
        # If we can find a better method to bring in objects to the class to send data to then good

    def send_data(self, data, dest_ip, type, dest_port):

        payload_segment = Transport(self.port, dest_port, type, data).encapsulate()
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
    
    # Incomign interface i beleive should not work this way (potentially looking at src_mac and finding it from there)
    def receive_frame(self, frame, incoming_interface):
        print(self.name, ": Layer 2: Frame recieved")
        print(self.name, ": Layer 2: Source MAC learned: ", frame["src_mac"])
        


        payload_packet = frame['payload_packet']
        print(self.name, ": Layer 2: Packet delivered to Network layer")
        print("\n\n")
        self.process_packet(payload_packet)
        return
    
    def handle_ack(self, ack_seq):
        return
    

    def attach_neighbour(self, ip, neighbour):
        self.neighbours[ip] = neighbour
    
    def process_packet(self, packet):
        print(self.name, ": Layer 3: Packet received from Data Link layer: SRC_IP ", packet["src_ip"], ", DST_IP ", packet["dest_ip"], ", TTL=", packet["ttl"])
        print(self.name, ": Layer 3: Destination IP read: ", packet["dest_ip"])


        if packet["dest_ip"] == self.ip:
            print(self.name, ": Layer 3: Packet identified as local delivery")
        else:
            print(self.name, ": Layer 3: Error IP is not meant for this host")
            return

        segment = packet["payload_segment"]
        print(self.name, ": Layer 3: Segment delivered to Transport Layer")
        print("\n\n")
        
        self.process_segment(segment, packet["src_ip"])

        return
    
    def process_segment(self, segment, src_ip):
        print(self.name, ": Layer 4:  Segment received from Network Layer")

        # Complete checksum in here (or in the segment object itself but we will need to do a lot of conversion to put it in object (something to think about))
        t = Transport(segment["src_port"], segment["dst_port"], segment["type"], segment["data"])

        if segment["checksum"] == t.checksum and segment["type"] == 0:
            print(f"{self.name}: Layer 4: Segment received form Network Layer")
            print(f"{self.name}: Layer 4: Data segment delivered to Application Layer. Data size={len(segment["data"])}")

            #ACK to send back to origional host
            self.send_data("", src_ip, 1, segment["src_port"])
        elif segment["type"] == 1:
            print(f"{self.name}: Layer 4: ACK received: seq={segment["seq"]}")
        return
    
    # Routing is different fom host to router so the function will be within their respective classes
    def routing(self, packet):
        dest_ip = packet['dest_ip']

        print(self.name,": Layer 3: Destination IP read: ", dest_ip)
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
        interface = self.discover_interface(frame)
        if interface == None:
            return
        
        print(self.name, ": Layer 2: Frame received on", interface)
        print(self.name, ": Layer 2: Source MAC learned:", frame["src_mac"], "on ", interface)
        
        payload_packet = frame['payload_packet']
        print(self.name, ": Layer 2: Packet delivered to Network Layer")
        print("\n\n")

        self.process_packet(payload_packet)
        return
    
    def process_packet(self, packet):
        print(self.name, ": Layer 3: Packet received from Data Link layer: SRC_IP ", packet["src_ip"], ", DST_IP ", packet["dest_ip"], ", TTL=", packet["ttl"])
        print(self.name, ": Layer 3: Destination IP read: ", packet["dest_ip"])

        packet['ttl'] -= 1
        print(f"{self.name}: Layer 3: TTL decremented: {packet['ttl']+1} → {packet["ttl"]}")


        interface, next_hop = self.routing(packet)
        print(f"{self.name}: Layer 3: Routing table lookup performed")
        print(f"{self.name}: Layer 3: Next-hop IP determined: {next_hop}")
        print(f"{self.name}: Layer 3: Outgoing interface selected ({interface})")
        print(f"{self.name}: Layer 3: Packet forwarded to Data Link Layer")

        print("\n\n")

        

        self.forward_packet(packet, interface, next_hop)
        return 
    
    def routing(self, packet):
        dest_ip = packet['dest_ip']

        print(self.name,": Layer 3: Destination IP read: ", dest_ip)
        for network, (interface, next_hop) in self.routing_table.items():
            if network != "default" and dest_ip.startswith(network):
                break
        else:
            interface, next_hop = self.routing_table["default"]
        
        return interface, next_hop
    
    def forward_packet(self, packet, outgoing_interface, next_hop):
        print(f"{self.name}: Layer 2: Packet received from Network Layer")
        dest_mac = self.mac_table_lookup(next_hop)

        print(f"{self.name}: Layer 2: Destination MAC lookup for next-hop IP {next_hop} → {dest_mac}")
        frame = Datalink(self.mac[outgoing_interface], dest_mac, "0x0800", packet).encapsulate()

        host = self.mac_obj_table[dest_mac]
        print(f"{self.name}: Layer 2: Frame forwarded on Interface 2")
        print("\n\n")
        host.receive_frame(frame, outgoing_interface)
        return
    
    def mac_table_lookup(self, next_hop):
        return self.mac_table[next_hop]
    
    # Again the only 2 ways i can think about doing this is a look (like now) or passign interface as a parameter (needs looking into)
    def discover_interface(self, incoming_frame):
        dest_mac = incoming_frame['dest_mac']
        curr_interface = None
        for interface, mac in self.mac.items():
            if mac == dest_mac:
                curr_interface = interface
                break

        if curr_interface == None:
            print(self.name, ": Error: Interface data sent to does not exist")
            return None
        return curr_interface
    