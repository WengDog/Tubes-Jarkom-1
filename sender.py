from socket import *

import packet
import sys
import random

sock = socket(AF_INET, SOCK_DGRAM)
host = "127.0.0.1"
port = 5005
MAX_DATA_SIZE = 32768 # 32kb
addr = (host,port)

fname = input("file name: ")
FILE_NAME =fname.encode()

f = open(fname, "rb")
DATA = f.read(MAX_DATA_SIZE)
i = 0
ID = random.randrange(15)

while(DATA):
  NEXT_DATA = f.read(MAX_DATA_SIZE)

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
  LENGTH = len(DATA).to_bytes(2, "big")

  # Make PACKET
  PACKET = packet.Packet(HEADER, SEQUENCE_NUMBER, LENGTH, DATA)
  PACKET.encode()
  sock.sendto(PACKET, addr)

  # Iterate
  DATA = NEXT_DATA
  i += 1

sock.close()
f.close()