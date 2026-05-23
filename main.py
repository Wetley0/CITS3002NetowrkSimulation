from devices import Host, Router
import config
import sys

class Main:
    # Defining and constructing Hosts and Router with predefined values set in config.py
    def __init__ (self):
        # Host A creation
        self.host_a = Host(config.HOST_A_NAME, config.HOST_A_ROUTING_TABLE, config.HOST_A_MAC_TABLE,config.HOST_A_IP,config.HOST_A_MAC)
        
        # Host B creation
        self.host_b = Host(config.HOST_B_NAME, config.HOST_B_ROUTING_TABLE, config.HOST_B_MAC_TABLE, config.HOST_B_IP, config.HOST_B_MAC)

        # Router Creation
        self.router = Router(
            config.R1_NAME,
            {config.R1_INTERFACE1: config.R1_MAC1, config.R1_INTERFACE2: config.R1_MAC2},
            config.R1_ROUTING_TABLE,
            config.R1_MAC_TABLE)
        
        # Set the object connecitons in the network (Allows connection between classes as if they were connected in a network)
        self.router.mac_obj_table = {"AA:AA:AA:AA:AA:AA": self.host_a, "DD:DD:DD:DD:DD:DD": self.host_b}
        self.host_a.mac_obj_table = {"BB:BB:BB:BB:BB:BB": self.router}
        self.host_b.mac_obj_table = {"CC:CC:CC:CC:CC:CC": self.router}
        return
    
    # Funciton to begin sending data from Host A to Host B
    def send_data(self, src_host, dest_host, data):
        src_host.send_data(data, dest_host.ip, 0, dest_host.port)

# Code begins here
if __name__ == "__main__":
    # The size of the message in bytes
    size = int(sys.argv[1])
    
    # Initialise application
    app = Main()

    # The network begins sending data
    # If you would like to change which host communicates to another swapping the objects around e.g. app.send_data(app.host_b, app.host_a, "A"*size)
    app.send_data(app.host_a, app.host_b, "A"*size)