class Frame:
    def __init__ (self, src_mac, dest_mac, type, payload_packet):
        self.src_mac = src_mac
        self.dest_mac = dest_mac
        self.type = type
        self.payload_packet = payload_packet

class Packet:
    def __init__ (self, src_ip, dest_ip, ttl, protocol, tot_len, payload_segment):
        self.src_ip = src_ip
        self.dest_ip = dest_ip
        self.ttl = ttl
        self.protocol = protocol
        self.tot_len = tot_len
        self.payload_segment = payload_segment

class Segment:
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
        return
    
    # Eventually will need some functions for segmentation and rdt2.2 and a way to max out at 50 bytes!!
