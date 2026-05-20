class Datalink:
    def __init__ (self, src_mac, dest_mac, type, payload_packet):
        self.src_mac = src_mac
        self.dest_mac = dest_mac
        self.type = type
        self.payload_packet = payload_packet

class Network:
    def __init__ (self, src_ip, dest_ip, protocol, tot_len, payload_segment):
        self.src_ip = src_ip
        self.dest_ip = dest_ip
        self.ttl = 100
        self.protocol = protocol
        self.tot_len = len(payload_segment)
        self.payload_segment = payload_segment
    
    def encapsulate(self):
        packet = {
            "src_ip": self.src_ip,
            "dest_ip": self.dest_ip,
            "ttl": self.ttl,
            "protocol": self.protocol
        }
        return packet

class DataLinkLayer:
    def __init__(self, mac_address, mac_table, name_node):
        self.mac_address = mac_address
        self.mac_table = mac_table
        self.name_node = name_node
    
    def recieve(self, frame):
        return    

class Transport:
    def __init__ (self, src_port, dest_port, type, data):
        self.src_port = src_port
        self.dest_port = dest_port
        
        # 0 fror data 1 for ACK
        self.type = type

        self.seq_num = 0
        self.data = data
        
        self.length = 10 + len(data)
        self.checksum = self.checksum_calc()

    def encapsulate(self):
        segment = {
            "src_port": self.src_port,
            "dst_port": self.dest_port,
            "length": self.length,
            "checksum": self.checksum,
            "type": self.type,   # 0 = DATA, 1 = ACK
            "seq": self.seq_num,
            "data": self.data
        }
        return segment
    
    def checksum_calc(self):
        # Adds up ASCII values for each letter in the message
        total = 0
        for letter in self.data:
            total += ord(letter)
        # Includes values of other values in message
        total += self.dest_port + self.src_port + self.seq_num

        # The maximum size has to be 2 byte number. Max 2 byte number is 65536, so this keeps it in the range
        return total % 65536
    
    # Eventually will need some functions for segmentation and rdt2.2 and a way to max out at 50 bytes!!
