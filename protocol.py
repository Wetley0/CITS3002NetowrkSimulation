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
    def __init__ (self, src_port, dest_port, type, data):
        self.src_port = src_port
        self.dest_port = dest_port
        
        # 0 fror data 1 for ACK
        self.type = type

        self.seq_num = 0
        self.data = data
        
        if isinstance(self.data, str):
            data_bytes = self.data.encode()
        else:
            data_bytes = self.data

        self.data_bytes = data_bytes
        
        self.length = 12 + len(data_bytes)
        self.checksum = self.checksum_calc()
    def encapsulate(self):
        packet = bytearray()

        packet += self.src_port.to_bytes(2, 'big')
        packet += self.dest_port.to_bytes(2, 'big')
        packet += self.length.to_bytes(2, 'big')
        packet += self.checksum.to_bytes(2, 'big')
        packet += self.type.to_bytes(2, 'big')
        packet += self.seq_num.to_bytes(2, 'big')
        
        # Plan to edit this later once i understand if data comes in bytes or not
        # data must be bytes
        # if isinstance(self.data, str):
        #     data_bytes = self.data.encode()
        # else:
        #     data_bytes = self.data

        packet += self.data_bytes
        return bytes(packet)
    
    def checksum_calc(self):
        total = 0

        # build all bytes
        fields = bytearray()
        fields += self.src_port.to_bytes(2, 'big')
        fields += self.dest_port.to_bytes(2, 'big')
        fields += self.length.to_bytes(2, 'big')
        fields += self.type.to_bytes(2, 'big')
        fields += self.seq_num.to_bytes(2, 'big')

        # Again plan to fix this later
        # if isinstance(self.data, str):
        #     data_bytes = self.data.encode()
        # else:
        #     data_bytes = self.data
        
        fields += self.data_bytes

        # sum all bytes
        for byte in fields:
            total += byte

        # wrap around (keep it 16-bit like UDP)
        total = (total & 0xFFFF) + (total >> 16)

        # one's complement (invert bits)
        checksum = ~total & 0xFFFF

        return checksum