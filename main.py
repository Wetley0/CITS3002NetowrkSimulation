from devices import Host, Router
from protocol import Frame, Packet, Segment
import config

class Main:
    def __init__ (self):
        self.host_a = Host("A", config.HOST_A_IP, config.HOST_A_MAC, "LAN1")
        self.host_b = Host("B", config.HOST_B_IP, config.HOST_B_MAC, "LAN2")

        self.router = Router("R1", {
            config.HOST_A_IP: ("LAN1", config.R1_IP),
            config.HOST_B_IP: ("LAN2", config.R2_IP),
        })
        return
    def send_data(self, src_host, dest_host, data):
        segment_init = Segment(src_host.port, dest_host.port, src_host.seq, data)
        segment = segment_init.encapsulate()
        packet = Packet(src_host.ip, dest_host.ip, 0, 0, 0, segment)
        
        # print(segment.length)
        # print(segment.data_bytes)
        # binary_list = [f"{b:08b}" for b in segment.data_bytes]
        # binary_string = " ".join(binary_list)
        # print(binary_string)

if __name__ == "__main__":
    app = Main()
    app.send_data(app.host_a, app.host_b, "Hello")