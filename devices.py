from protocol import Transport, Network, Datalink
class Host:
    # Initialisation for Host object
    def __init__(self, name, routing_table, mac_table, ip, mac, mac_obj_table={}, port=8000):
        self.name = name
        self.ip = ip
        self.mac = mac
        self.port = port
        self.mac_table = mac_table
        self.routing_table = routing_table

        # Table conaining immidiate connection objects
        self.mac_obj_table = mac_obj_table

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
        first_500_bytes = data[:500]
        self.remaining_data = data[500:]

        print(f"{self.name}: Layer 4: Data received from Application Layer. Data size={len(data)}")
        checksum = self.checksum_calc(first_500_bytes, dest_port, self.port, self.seq)
        print(f"{self.name}: Layer 4: Checksum computed")
        
        self.dest_ip = dest_ip
        self.unacknowledged_data = {"data": first_500_bytes, "dest_ip": dest_ip, "type" : type, "dest_port" : dest_port, "seq": self.seq, "checksum": checksum}

        return self.send_500_bytes(first_500_bytes, dest_ip, type, dest_port, self.seq, checksum)

    # Send the data in 500 byte chunks if data reaches over 500
    def send_500_bytes(self, data, dest_ip, type, dest_port, seq_num, checksum):
        # Allow for consistent log output
        types = {0: "DATA", 1: "ACK"}

        # Encapsulating on Transport Layer to create a segment
        payload_segment = Transport(self.port, dest_port, type, data, checksum, seq_num).encapsulate()
        print(f"{self.name}: Layer 4: Segment created by adding transport layer header ({types[type]}, seq={seq_num}) (encapsulation)")
        print(f"{self.name}: Layer 4: Segment sent to Network Layer")
        print("\n\n")

        # Encapsulating on Netowkr Layer to create a packet
        packet = Network(self.ip, dest_ip, 17, 0, payload_segment).encapsulate()
        print(f"{self.name}: Layer 3: Segment received from Transport Layer: SRC_IP={packet["src_ip"]}, DST_IP={packet["dest_ip"]}, TTL={packet["ttl"]}")
        print(f"{self.name}: Layer 3: Destination IP read: {packet["dest_ip"]}")
        
        # Use routing table to find the next ip hop
        next_hop = self.routing(packet)
        print(f"{self.name}: Layer 3: Routing table lookup performed")
        print(f"{self.name}: Layer 3: Next-hop IP determined: {next_hop}")
        print(f"{self.name}: Layer 3: Outgoing interface selected")
        print(f"{self.name}: Layer 3: Packet forwarded to Data Link Layer")
        print("\n\n")

        # Encapsulate on Data Link Layer to create a frame
        # Keep in mind for later I am passing the next hop and interface as parameters. (that do not go in init of datalink object) I do not know how you are meant to actually do so check this later when working
        print(f"{self.name}: Layer 2: Packet received from Network Layer")
        # Finf destination MAC
        dest_mac = self.mac_table_lookup(next_hop)
        print(f"{self.name}: Layer 2: Destination MAC lookup for next-hop IP ({next_hop}) → {dest_mac}")
        # Frame creation
        frame = Datalink(self.mac, dest_mac, "0x0800", packet).encapsulate()
        print(f"{self.name}: Layer 2: Frame created: SRC_MAC={frame["src_mac"]}, DST_MAC={frame["dest_mac"]}")
        # Find router object to send frame
        router = self.mac_obj_table[dest_mac]
        print(f"{self.name}: Layer 2: Frame sent")
        print("\n\n")
        # Sending frame to router
        return router.receive_frame(frame)

    # Host recieves a frame from a router
    def receive_frame(self, frame):
        print(f"{self.name}: Layer 2: Frame received")
        print(f"{self.name}: Layer 2: Source MAC learned: {frame["src_mac"]}")
        
        # Unpack frame to obtain packet
        payload_packet = frame['payload_packet']
        print(f"{self.name}: Layer 2: Packet delivered to Network Layer")
        print("\n\n")

        # Begin to process packet
        return self.process_packet(payload_packet)
    
    # Begin processesing received packet
    def process_packet(self, packet):
        print(f"{self.name}: Layer 3: Packet received from Data Link Layer: SRC_IP={packet["src_ip"]}, DST_IP={packet["dest_ip"]}, TTL={packet["ttl"]}")
        print(f"{self.name}: Layer 3: Destination IP read: {packet["dest_ip"]}")

        # If the IP was not meant for this host error and exit
        if packet["dest_ip"] == self.ip:
            print(f"{self.name}: Layer 3: Packet identified as local delivery")
        else:
            print(f"{self.name}: Layer 3: Error IP is not meant for this host")
            return

        # Unpack packet to obtain segment
        segment = packet["payload_segment"]
        print(f"{self.name}: Layer 3: Segment delivered to Transport Layer")
        print("\n\n")
        
        # Begin to process segment
        return self.process_segment(segment, packet["src_ip"])
    
    # Begin processesing received segment
    def process_segment(self, segment, src_ip):
        # Calculate received checksum locally
        checksum = self.checksum_calc(segment["data"], segment["dest_port"], segment["src_port"], segment["seq_num"])
        print(f"{self.name}: Layer 4: Segment received from Network Layer")
        
        # Compare checksums (error out if they do not match)
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

    # Handle received ACK
    def handle_ack(self, ack_num):
        # If the number is what we expect continue, if not send previous data again
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

    # Routing function to obtain next hop
    def routing(self, packet):
        dest_ip = packet['dest_ip']

        # Loop though the routing table to find a match or just use default path
        for network, next_hop in self.routing_table.items():
            if network != "default" and dest_ip.startswith(network):
                break
        else:
            next_hop = self.routing_table["default"]
        
        return next_hop
    
    # Simple one line mac table look up as it is a simple dictionary
    def mac_table_lookup(self, next_hop):
        return self.mac_table[next_hop]
    
    # Calculate checksum upon send or receiving data
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
    # Initialisaiton of the router
    def __init__(self, name, mac, routing_table, mac_table, mac_obj_table={}):
        self.name = name
        self.mac = mac
        self.routing_table = routing_table
        self.mac_table = mac_table
        self.mac_obj_table = mac_obj_table
    
    # Router recieves a frame from a Host
    def receive_frame(self, frame):
        # Discover which interface received the frame
        interface = self.discover_interface(frame)
        if interface == None:
            return
        print(f"{self.name}: Layer 2: Frame received on {interface}")
        print(f"{self.name}: Layer 2: Source MAC learned: {frame["src_mac"]} on {interface}")
        
        # Unpack frame to obtain packet
        payload_packet = frame['payload_packet']
        print(f"{self.name}: Layer 2: Packet delivered to Network Layer")
        print("\n\n")

        # Begin processing packet
        return self.process_packet(payload_packet)
    
    # Begin processing receieved packet
    def process_packet(self, packet):
        print(f"{self.name}: Layer 3: Packet received from Data Link Layer: SRC_IP={packet["src_ip"]}, DST_IP={packet["dest_ip"]}, TTL={packet["ttl"]}")
        print(f"{self.name}: Layer 3: Destination IP read: {packet["dest_ip"]}")

        # Handle TTL
        packet['ttl'] -= 1
        if packet['ttl'] == 0:
            print(f"{self.name}: Layer 3: Error TTL has reached the end of it's lifecycle")
            return
        print(f"{self.name}: Layer 3: TTL decremented: {packet['ttl']+1} → {packet["ttl"]}")

        # Find the next hop and interface it will occur
        interface, next_hop = self.routing(packet)
        print(f"{self.name}: Layer 3: Routing table lookup performed")
        print(f"{self.name}: Layer 3: Next-hop IP determined: {next_hop}")
        print(f"{self.name}: Layer 3: Outgoing interface selected ({interface})")
        print(f"{self.name}: Layer 3: Packet forwarded to Data Link Layer")

        print("\n\n")
        
        # Begin to forward the packet to next_hop
        return self.forward_packet(packet, interface, next_hop)
    
    # Routing handling
    def routing(self, packet):
        # Set destinaiton IP
        dest_ip = packet["dest_ip"]

        # Loop thorugh the routing table
        for network, (interface, next_hop) in self.routing_table.items():

            # Match subnet
            if dest_ip.startswith(network):

                # Directly connected network
                if next_hop == "DIRECT":
                    next_hop = dest_ip

                return interface, next_hop

        # Default route to Interface 1 (will not stop error but will garentee a route is created)
        return self.routing_table["10.0.1"]
    
    # Forward the packet to next hop
    def forward_packet(self, packet, outgoing_interface, next_hop):
        print(f"{self.name}: Layer 2: Packet received from Network Layer")
        # Find the MAC address of next hop
        dest_mac = self.mac_table_lookup(next_hop)

        print(f"{self.name}: Layer 2: Destination MAC lookup for next-hop IP ({next_hop}) → {dest_mac}")
        # Create frame
        frame = Datalink(self.mac[outgoing_interface], dest_mac, "0x0800", packet).encapsulate()
        print(f"{self.name}: Layer 2: Frame created: SRC_MAC={self.mac[outgoing_interface]}, DST_MAC={dest_mac}")

        # Set the host object to send frame to
        host = self.mac_obj_table[dest_mac]
        print(f"{self.name}: Layer 2: Frame forwarded on {outgoing_interface}")
        print("\n\n")
        return host.receive_frame(frame)
    

    # MAC table lookup
    def mac_table_lookup(self, next_hop):
        return self.mac_table[next_hop]
    
    # Simple function to know what interface the router is receiving on
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