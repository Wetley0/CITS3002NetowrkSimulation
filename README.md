# CITS3002 Network Simulation

A python simulation of how a packet travels through a simplified OSI network. From application data down to Ethernet frames.

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
- Message fragmentation, data exceeding 490 bytes is split and sent one after another

## Usage

```bash
python main.py <message_size>
```

Where `<message_size>` is the number of bytes to send. For example:

```bash
python main.py 500
```

Any message larger than 490 bytes is automatically fragmented into 490 byte sections and sent across multiple segments. The output is printed out showing each layer's processing steps as the data travels from source to destination.

