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
        self.protocol = protocol
        self.tot_len = tot_len
        self.payload_segment = payload_segment

class Segment:
    def __init__ (self, src_port, dest_port, length, checksum, type, seq_num, data):
        self.src_port = src_port
        self.dest_port = dest_port
        self.length = length
        self.checksum = checksum
        self.type = type
        self.seq_num = seq_num
        self.data = data