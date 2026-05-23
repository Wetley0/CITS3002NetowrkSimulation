from protocol import Transport, Network, Datalink
class Host:
    def __init__(self, name, routing_table, mac_table, ip, mac, mac_obj_table={}, port=8000):
        self.name = name
        self.ip = ip
        self.mac = mac
        # Removing network as it is not being used but keeping it in case we need to bring it back
        # self.network = network
        self.port = port
        self.mac_table = mac_table
        self.routing_table = routing_table

        # For now maybe for good not sure but this will hold a dictionary of the objects connected to hosts
        self.mac_obj_table = mac_obj_table
        # If we can find a better method to bring in objects to the class to send data to then good

        # RDT2.2 LOGIC
        self.dest_ip = "" # Problem if more than one node is sending info to us
        # Logic for when data size is over 500
        self.remaining_data = ""
        self.unacknowledged_data = None

        self.seq = 0 # When correct ACK recieved change this

        # Remove this as we only need the one seq number
        self.expected_ack = 0 # Dont know if this is required, similar to seq but include for readability

    # Call self.send_data(self.remaining_data,...) when ACK successful and there is still remaining data, and change seq num and expected_ack

    # Seperates segment into 500 byte chunks and prepares for next segment to be sent, and possible failures according to RDT2.2
    def send_data(self, data, dest_ip, type, dest_port):
        first_490_bytes = data[:490]
        self.remaining_data = data[490:]

        print(f"{self.name}: Layer 4: Data received from Application Layer. Data size={len(data)}")
        checksum = self.checksum_calc(first_490_bytes, dest_port, self.port, self.seq)
        print(f"{self.name}: Layer 4: Checksum computed")
        
        self.dest_ip = dest_ip
        self.unacknowledged_data = {"data": first_490_bytes, "dest_ip": dest_ip, "type" : type, "dest_port" : dest_port, "seq": self.seq, "checksum": checksum}

        return self.send_500_bytes(first_490_bytes, dest_ip, type, dest_port, self.seq, checksum)


    def send_500_bytes(self, data, dest_ip, type, dest_port, seq_num, checksum):

        types = {0: "DATA", 1: "ACK"}

        payload_segment = Transport(self.port, dest_port, type, data, checksum, seq_num).encapsulate()
        print(f"{self.name}: Layer 4: Segment created by adding Transport Layer header ({types[type]}, seq={self.seq}) (encapsulation)")
        print(f"{self.name}: Layer 4: Segment sent to Network Layer")
        print("\n\n")

        packet = Network(self.ip, dest_ip, 17, 0, payload_segment).encapsulate()
        print(f"{self.name}: Layer 3: Segment received from Transport Layer: SRC_IP={packet["src_ip"]}, DST_IP={packet["dest_ip"]}, TTL={packet["ttl"]}")
        print(f"{self.name}: Layer 3: Destination IP read: {packet["dest_ip"]}")
        next_hop = self.routing(packet)
        print(f"{self.name}: Layer 3: Routing table lookup performed")
        print(f"{self.name}: Layer 3: Next-hop IP determined: {next_hop}")
        print(f"{self.name}: Layer 3: Outgoing interface selected")
        print(f"{self.name}: Layer 3: Packet forwarded to Data Link Layer")
        print("\n\n")

        # Keep in mind for later I am passing the next hop and interface as parameters. (that do not go in init of datalink object) I do not know how you are meant to actually do so check this later when working
        # Also we may not need interface in the routing tables for hosts but now it is just a blank string maybe delete later
        print(f"{self.name}: Layer 2: Packet received from Network Layer")
        dest_mac = self.mac_table_lookup(next_hop)
        print(f"{self.name}: Layer 2: Destination MAC lookup for next-hop IP ({next_hop}) → {dest_mac}")
        frame = Datalink(self.mac, dest_mac, "0x0800", packet).encapsulate()
        print(f"{self.name}: Layer 2: Frame created: SRC_MAC={frame["src_mac"]}, DST_MAC={frame["dest_mac"]}")
        router = self.mac_obj_table[dest_mac]
        print(f"{self.name}: Layer 2: Frame sent")
        print("\n\n")
        return router.receive_frame(frame)
    
    # maybe add logic if the mac address does not match the mac address of this host
    # Incomign interface i beleive should not work this way (potentially looking at src_mac and finding it from there)
    def receive_frame(self, frame):
        print(f"{self.name}: Layer 2: Frame received")
        print(f"{self.name}: Layer 2: Source MAC learned: {frame["src_mac"]}")
        
        payload_packet = frame['payload_packet']
        print(f"{self.name}: Layer 2: Packet delivered to Network Layer")
        print("\n\n")
        return self.process_packet(payload_packet)

    def attach_neighbour(self, ip, neighbour):
        self.neighbours[ip] = neighbour
    
    def process_packet(self, packet):

        print(f"{self.name}: Layer 3: Packet received from Data Link Layer: SRC_IP={packet["src_ip"]}, DST_IP={packet["dest_ip"]}, TTL={packet["ttl"]}")
        print(f"{self.name}: Layer 3: Destination IP read: {packet["dest_ip"]}")


        if packet["dest_ip"] == self.ip:
            print(f"{self.name}: Layer 3: Packet identified as local delivery")
        else:
            print(f"{self.name}: Layer 3: Error IP is not meant for this host")
            return

        segment = packet["payload_segment"]
        print(f"{self.name}: Layer 3: Segment delivered to Transport Layer")
        print("\n\n")
        
        return self.process_segment(segment, packet["src_ip"])
    
    def process_segment(self, segment, src_ip):
        checksum = self.checksum_calc(segment["data"], segment["dest_port"], segment["src_port"], segment["seq_num"])
        print(f"{self.name}: Layer 4: Segment received form Network Layer")

        if segment["checksum"] == checksum:
            print(f"{self.name}: Layer 4: Checksum verified")

            # The Host has recieved DATA
            # No need to check if data is a retransmission of old data because "No frame corruption"
            if segment["type"] == 0:
                print(f"{self.name}: Layer 4: DATA segment delivered to Application Layer. Data size={len(segment["data"])}")

                # Create ACK message, and give back to sender 
                ACK_checksum = self.checksum_calc("", segment["src_port"], segment["dest_port"], segment["seq_num"])
                return self.send_500_bytes("", src_ip, 1, segment["src_port"], segment["seq_num"], ACK_checksum)

            # The Host has recieved ACK
            elif segment["type"] == 1:
                return self.handle_ack(segment["seq_num"])

        # Invalide Checksum meaning that it is ignored and handled by timeout
        else:
            print(f"{self.name}: Layer 4: Invalid Checksum")
            return


    def handle_ack(self, ack_num):
        if ack_num == self.expected_ack:
            print(f"{self.name}: Layer 4: ACK received: seq={ack_num}")

            self.seq = 1 - self.seq
            self.expected_ack = 1 - self.expected_ack

            if self.remaining_data != "":
                return self.send_data(self.remaining_data, self.dest_ip, 0, self.unacknowledged_data["dest_port"])
    
        else:
            print(f"{self.name}: Layer 4: Incorrect ACK received, retransmitting segment")
            return self.send_500_bytes(
                self.unacknowledged_data["data"],
                self.unacknowledged_data["dest_ip"],
                self.unacknowledged_data["type"],
                self.unacknowledged_data["dest_port"],
                self.unacknowledged_data["seq"],
                self.unacknowledged_data["checksum"]
            )

    # Routing is different fom host to router so the function will be within their respective classes
    def routing(self, packet):
        dest_ip = packet['dest_ip']

        for network, next_hop in self.routing_table.items():
            if network != "default" and dest_ip.startswith(network):
                break
        else:
            next_hop = self.routing_table["default"]
        
        return next_hop
    
    # Debugs will needed to be added to this later (like what is that ip address does not exist in mac_table so on)
    def mac_table_lookup(self, next_hop):
        return self.mac_table[next_hop]
    
    def checksum_calc(self, data, dest_port, src_port, seq_num):
        # Adds up ASCII values for each letter in the message
        total = 0
        for letter in data:
            total += ord(letter)
        # Includes values of other values in message
        total += dest_port + src_port + seq_num

        # The maximum size has to be 2 byte number. Max 2 byte number is 65536, so this keeps it in the range
        return total % 65536


class Router:
    def __init__(self, name, mac, routing_table, mac_table, mac_obj_table={}):
        self.name = name
        self.mac = mac
        self.routing_table = routing_table
        self.mac_table = mac_table
        self.mac_obj_table = mac_obj_table
    
    def receive_frame(self, frame):
        interface = self.discover_interface(frame)
        if interface == None:
            return
        print(f"{self.name}: Layer 2: Frame received on {interface}")
        print(f"{self.name}: Layer 2: Source MAC learned: {frame["src_mac"]} on {interface}")
        
        payload_packet = frame['payload_packet']
        print(f"{self.name}: Layer 2: Packet delivered to Network Layer")
        print("\n\n")

        return self.process_packet(payload_packet)
    
    def process_packet(self, packet):
        print(f"{self.name}: Layer 3: Packet received from Data Link Layer: SRC_IP={packet["src_ip"]}, DST_IP={packet["dest_ip"]}, TTL={packet["ttl"]}")
        print(f"{self.name}: Layer 3: Destination IP read: {packet["dest_ip"]}")

        packet['ttl'] -= 1
        if packet['ttl'] == 0:
            print(f"{self.name}: Layer 3: Error TTL has reached the end of it's lifecycle")
            return
        print(f"{self.name}: Layer 3: TTL decremented: {packet['ttl']+1} → {packet["ttl"]}")


        interface, next_hop = self.routing(packet)
        print(f"{self.name}: Layer 3: Routing table lookup performed")
        print(f"{self.name}: Layer 3: Next-hop IP determined: {next_hop}")
        print(f"{self.name}: Layer 3: Outgoing interface selected ({interface})")
        print(f"{self.name}: Layer 3: Packet forwarded to Data Link Layer")

        print("\n\n")

        return self.forward_packet(packet, interface, next_hop)
    
    def routing(self, packet):
        dest_ip = packet["dest_ip"]

        for network, (interface, next_hop) in self.routing_table.items():

            # Match subnet
            if dest_ip.startswith(network):

                # Directly connected network
                if next_hop == "DIRECT":
                    next_hop = dest_ip

                return interface, next_hop

        # Default route
        return self.routing_table["default"]
    
    def forward_packet(self, packet, outgoing_interface, next_hop):
        print(f"{self.name}: Layer 2: Packet received from Network Layer")
        dest_mac = self.mac_table_lookup(next_hop)

        print(f"{self.name}: Layer 2: Destination MAC lookup for next-hop IP ({next_hop}) → {dest_mac}")
        frame = Datalink(self.mac[outgoing_interface], dest_mac, "0x0800", packet).encapsulate()
        print(f"{self.name}: Layer 2: Frame created: SRC_MAC={self.mac[outgoing_interface]}, DST_MAC={dest_mac}")

        host = self.mac_obj_table[dest_mac]
        print(f"{self.name}: Layer 2: Frame forwarded on {outgoing_interface}")
        print("\n\n")
        return host.receive_frame(frame)
    
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