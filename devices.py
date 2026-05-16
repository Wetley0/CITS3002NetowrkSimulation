class Host:
    def __init__(self, name, ip, mac, network):
        self.name = name
        self.ip = ip
        self.mac = mac
        self.network = network
        self.seq = 0
    def send_data(self, data, dest_ip):
        return
    def receive(self, frame):
        return
    def handle_ack(self, ack_seq):
        return

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