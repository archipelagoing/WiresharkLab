#!/usr/bin/python3

from scapy.all import *
import sys
import time
import math

# make sure to load the HTTP layer
load_layer("http")
pcap_filename = "pcap1.pcap"

# example counters
number_of_packets_total = 0
number_of_tcp_packets = 0
number_of_udp_packets = 0

processed_file = rdpcap(pcap_filename)# read in the pcap file
sessions = processed_file.sessions() #get the list of sessions/TCP connections
for session in sessions:
    for packet in sessions[session]: # for each packet in each session
        number_of_packets_total = number_of_packets_total + 1 #increment total packet count
        if packet.haslayer(TCP): # check is the packet is a TCP packet
            number_of_tcp_packets = number_of_tcp_packets + 1 # count TCP packets
            source_ip = packet[IP].src # note that a packet is represented as a python hash table with keys corresponding to
            dest_ip = packet[IP].dst # layer field names and the values of the hash table as the packet field values


            if (packet.haslayer(HTTP)): # test for an HTTP packet
                if HTTPRequest in packet:
                    arrival_time = packet.time # get unix time of the packet
                    print ("Got a TCP packet part of an HTTP request at time:%0.4f for server IP %s" % (arrival_time,dest_ip))
            else:
                if packet.haslayer(UDP):
                    number_of_udp_packets = number_of_udp_packets + 1
                    print("Got %d packets total, %d TCP packets and %d UDP packets" % (number_of_packets_total, number_of_tcp_packets,number_of_udp_packets))
