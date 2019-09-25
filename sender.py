from socket import *

import sys
import random

sock = socket(AF_INET, SOCK_DGRAM)
host = "127.0.0.1"
port = 5005
MAX_DATA_SIZE = 32768 # 32kb
addr = (host,port)

fname =sys.argv[1].encode()

f = open(fname, "rb")
DATA = f.read(MAX_DATA_SIZE)
NEXT_DATA = f.read(MAX_DATA_SIZE)
i = 0

while(len(NEXT_DATA) != 0):
  # Make header
  TYPE = "00000000"
  ID = random.randrange(15)
  str_header = TYPE + format(ID, "08b")
  HEADER = int(str_header).to_bytes(1,"big")

  # Make sequence number
  SEQUENCE_NUMBER = i.to_bytes(2,"big")

  # Make length
  LENGTH = len(DATA).to_bytes(2,"big")

  # Make Checksum
  temp = HEADER + SEQUENCE_NUMBER + LENGTH + DATA
  


  DATA = NEXT_DATA
  NEXT_DATA = f.read(MAX_DATA_SIZE)
  i += 1

sock.close()
f.close()