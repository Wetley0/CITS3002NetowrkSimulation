class Frame:
    def __init__ (self, src_mac, dest_mac, type, payload_packet):
        src_mac = self.src_mac
        dest_mac = self.dest_mac
        type = self.type
        payload_packet = self.payload_packet

class Packet:
    def __init__ (self, src_ip, dest_ip, ttl, protocol, tot_len, payload_segment):
        src_ip = self.src_mac
        dest_ip = self.dest_mac
        ttl = self.type
        protocol = self.protocol
        tot_len = self.tot_len
        payload_segment = self.payload_segment

class Segment:
    def __init__ (self, src_port, dest_port, length, checksum, type, seq_num, data):
        src_port = self.src_port
        dest_port = self.dest_port
        length = self.length
        checksum = self.checksum
        type = self.type
        seq_num = self.seq_num
        data = self.data