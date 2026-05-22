from devices import Host, Router
from protocol import Datalink, Network, Transport
import config
import sys

class Main:
    def __init__ (self):
        self.host_a = Host("Host A",
                        {"10.0.1": ("", "10.0.1.10"),"default": ("", "10.0.1.1")},
                        {"10.0.1.1": "BB:BB:BB:BB:BB:BB"},
                        config.HOST_A_IP,
                        config.HOST_A_MAC,
                        "LAN1")
        
        self.host_b = Host("Host B", {"default": ("", "10.0.2.1")}, {"10.0.2.1": "CC:CC:CC:CC:CC:CC"}, config.HOST_B_IP, config.HOST_B_MAC, "LAN2")

        # Setting up names based on the interface (dictionary type)
        self.router = Router(
            {"Interface1": "Router R1", "Interface2": "Router R2"},

            {
                "Interface1": "BB:BB:BB:BB:BB:BB",
                "Interface2": "CC:CC:CC:CC:CC:CC"
            },

            {
                "10.0.1": ("Interface1", "DIRECT"),
                "10.0.2": ("Interface2", "DIRECT"),
            },

            {
                "10.0.1.10": "AA:AA:AA:AA:AA:AA",
                "10.0.2.20": "DD:DD:DD:DD:DD:DD"
            },

            {
                "AA:AA:AA:AA:AA:AA": self.host_a,
                "DD:DD:DD:DD:DD:DD": self.host_b
            }
        )

        self.host_a.mac_obj_table = {"BB:BB:BB:BB:BB:BB": self.router}
        self.host_b.mac_obj_table = {"CC:CC:CC:CC:CC:CC": self.router}
        

        return
    def send_data(self, src_host, dest_host, data):
        src_host.send_data(data, dest_host.ip, 0, dest_host.port, 0)

if __name__ == "__main__":
    size = int(sys.argv[1])
    app = Main()
    app.send_data(app.host_a, app.host_b, "A"*size)