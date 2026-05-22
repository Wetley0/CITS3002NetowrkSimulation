from devices import Host, Router
from protocol import Datalink, Network, Transport
import config
import sys

class Main:
    def __init__ (self):
        self.host_a = Host(config.HOST_A_NAME, config.HOST_A_ROUTING_TABLE, config.HOST_A_MAC_TABLE,config.HOST_A_IP,config.HOST_A_MAC)
        
        self.host_b = Host(config.HOST_B_NAME, config.HOST_B_ROUTING_TABLE, config.HOST_B_MAC_TABLE, config.HOST_B_IP, config.HOST_B_MAC)

        # Setting up names based on the interface (dictionary type)
        self.router = Router(
            {config.R1_INTERFACE: config.R1_NAME, config.R2_INTERFACE: config.R2_NAME},
            {config.R1_INTERFACE: config.R1_MAC, config.R2_INTERFACE: config.R2_MAC},
            config.R_ROUTING_TABLE,
            config.R_MAC_TABLE)
        
        # Set the object connecitons in the network
        self.router.mac_obj_table = {"AA:AA:AA:AA:AA:AA": self.host_a, "DD:DD:DD:DD:DD:DD": self.host_b}
        self.host_a.mac_obj_table = {"BB:BB:BB:BB:BB:BB": self.router}
        self.host_b.mac_obj_table = {"CC:CC:CC:CC:CC:CC": self.router}
        return
    
    def send_data(self, src_host, dest_host, data):
        src_host.send_data(data, dest_host.ip, 0, dest_host.port)

if __name__ == "__main__":
    size = int(sys.argv[1])
    app = Main()
    app.send_data(app.host_a, app.host_b, "A"*size)