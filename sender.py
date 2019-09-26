from socket import *

import packet
import sys
import random

sender = socket(AF_INET, SOCK_DGRAM)
port = input("Port: ")
host = input("Host: ")
addr = (host,int(port))

fname = input("file name: ")
FILE_NAME =fname.encode()

f = open(fname, "rb")
DATA = f.read(packet.MAX_DATA_SIZE)
i = 0
ID = random.randrange(15)

while(DATA):
  NEXT_DATA = f.read(packet.MAX_DATA_SIZE)

  # Selama bukan paket terakhir
  if(len(NEXT_DATA) != 0):
    TYPE = "0000"
  else:
    TYPE = "0010"
  
  # Make HEADER = TYPE + ID
  str_header = TYPE + format(ID, "04b")
  HEADER = int(str_header,2).to_bytes(1,"big")

  # Make SEQUENCE_NUMBER
  SEQUENCE_NUMBER = i.to_bytes(2, "big")

  # Make LENGTH
  LENGTH = (len(DATA) // 1000).to_bytes(2, "big")

  # Make PACKET
  PACKET = packet.Packet(HEADER, SEQUENCE_NUMBER, LENGTH, DATA).encode()
  sender.sendto(PACKET, addr)

  # Wait response
  reply, addr = sender.recvfrom(packet.MAX_PACKET_SIZE)
  # print(int.from_bytes(reply[1:3], byteorder="big") + "/" + ))

  # Iterate
  DATA = NEXT_DATA
  i += 1

  REPLY_TYPE = int.from_bytes(reply[0:1], byteorder="big") >> 4

  if(REPLY_TYPE == packet.FIN_ACK):
    print("file with ID", ID, "sent!")

sender.close()
f.close()