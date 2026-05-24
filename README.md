# CITS3002 Network Simulation

A python simulation of how a packet travels through a simplified OSI network. From application data down to Ethernet frames.

## Contributors
| Name | Student Number |
|------|----------------|
| Wesley Conti | 23499047 |
| Andrew Gibson | 23865288 |

## Assumptions

Some portions of the assignment led to some room for interpretation so we will be assuming the following:
- It states that this assignment is logical simulation only so we assume we do not need to convert the encapsultated data into bytes.
- It also states this assignemnt it is assumed no packet, frame corruption, and all transmissions are deterministic. therefore, a time out property (for rdt2.2) will not be necessary iand not implemented.
- Since this is a fixed network the router routes only to hosts, not other routers.

## File Structure

| File | Description |
|------|-------------|
| `main.py` | Entry point, builds topology and controls messages |
| `config.py` | All static network config (IPs, MACs, routing tables) |
| `devices.py` | Host and Router class definitions |
| `protocol.py` | Transport, Network, and Datalink encapsulation classes |

## Architecture

Data is encapsulated layer by layer on the sending side, and decapsulated in reverse on the receiving side.

**Hosts** go through all three layers when sending and receiving:

| Layer | Name | Responsibilities |
|-------|------|-----------------|
| 4 | Transport | Segmentation, checksum, sequence numbers, ACK handling |
| 3 | Network | IP routing, TTL, packet forwarding |
| 2 | Data Link | MAC framing, interface and MAC table lookup |

**Routers** only ever operate up to layer 3. They recieve a frame at layer 2, utilise MAC tables to make a forwarding decision at layer 3, and send a new frame back up to layer 2. They do not process the transport layer. 

## Key Concepts Simulated

- Encapsulation and decapsulation at each OSI layer
- Routing table lookups and determing the next hop
- MAC address table lookups for layer 2 frame delivery
- 16-bit checksum calculation and validation, meaning modulo 65536 required.
- Stop and wait with alternating sequence numbers 0 and 1
- ACK handling
- TTL decrement and expiry at routers
- Message fragmentation, data exceeding 500 bytes is split and sent one after another

## Usage

```bash
python main.py <message_size>
```

Where `<message_size>` is the number of bytes to send. For example:

```bash
python main.py 500
```

The message sent will be a message from Host A to Host B. To change the host connection simply swap them in main.py

Any message larger than 500 bytes is automatically fragmented into 500 byte sections and sent across multiple segments. The output is printed out showing each layer's processing steps as the data travels from source to destination.

