from devices import Host, Router
from protocol import Datalink, Network, Transport
import config

class Main:
    def __init__ (self):
        self.host_a = Host("Host A",
                        {"10.0.1": ("", "10.0.1.10"),"default": ("", "10.0.1.1")},
                        {"10.0.1.1": "BB:BB:BB:BB:BB:BB"},
                        config.HOST_A_IP,
                        config.HOST_A_MAC,
                        "LAN1")
        
        self.host_b = Host("Host B", {"default": "10.0.2.1"}, {"10.0.2.1": "BB:BB:BB:BB:BB:BB"}, config.HOST_B_IP, config.HOST_B_MAC, "LAN2")


        self.router = Router("R1", {
            config.HOST_A_IP: ("LAN1", config.R1_IP),
            config.HOST_B_IP: ("LAN2", config.R2_IP),
        })

        self.host_a.mac_obj_table = {"BB:BB:BB:BB:BB:BB": self.router}
        self.host_b.mac_obj_table = {"CC:CC:CC:CC:CC:CC": self.router}
        self.router.mac_obj_table = {"AA:AA:AA:AA:AA:AA": self.host_a, "DD:DD:DD:DD:DD:DD": self.host_b}

        return
    def send_data(self, src_host, dest_host, data):
        src_host.send_data(data, dest_host.ip, dest_host.port)
        
        # segment_init = Transport(src_host.port, dest_host.port, src_host.seq, data)
        # segment = segment_init.encapsulate()
        # packet_init = Network(src_host.ip, dest_host.ip, 17, 0, segment)
        # packet = packet_init.encapsulate()
        # frame = Datalink()

        # R1_datalink = Datalink
        # R1_recieve = R1_datalink.recieve_frame(frame)

        # print(segment.length)
        # print(segment.data_bytes)
        # binary_list = [f"{b:08b}" for b in segment.data_bytes]
        # binary_string = " ".join(binary_list)
        # print(binary_string)

if __name__ == "__main__":
    app = Main()
    app.send_data(app.host_a, app.host_b, "Hello")