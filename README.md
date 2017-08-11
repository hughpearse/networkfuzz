networkfuzz
=========

Description:
Simple TCP/UDP pcap fuzzer

Introduction:
Most network fuzzing programs fuzz the Ethernet frame header, IP Header or TCP/UDP header. This is suitable for testing the network stack on the test machine but not suitable for testing the target applicaton for errors.

When other network fuzzers do modify the TCP/UDP payload, they tend to require the client application to be configured to use a proxy. A proxy fuzzer is suitable for a mature program such as a browser but is not suitable for DLL files that acquire their own sockets dynamically.

This program solves these 2 problems by fuzzing the payload data in a Pcap file and writing the fuzzed Pcap file out to disk. The new modified Pcap can then be replayed using tcpreplay.

Note: the transformation python hooks are located in the "hooks" subdirectory.

**Example Usage:**
- ./RUN.sh -i inputfile -o outputfile -t data-transformation-python-module
- ./RUN.sh -i sample.pcap -o ./result.pcap -t example
- sudo tcpreplay -i em1 ./result.pcap

