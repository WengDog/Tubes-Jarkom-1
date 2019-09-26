import socket
import packet

receiver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
port = input("Port: ")
host = input("Host: ")
addr = (host, int(port))
receiver.bind(addr)
DATA_FILE = b''

while True:
  data,addr = receiver.recvfrom(packet.MAX_PACKET_SIZE)
  
  # get packet data
  HEADER = data[0:1]
  TYPE = int.from_bytes(HEADER, byteorder="big") >> 4
  ID = int.from_bytes(HEADER, byteorder="big") & 0x0f
  SEQUENCE_NUMBER = data[1:3]
  LENGTH = data[3:5]
  CHECKSUM = data[5:7]
  DATA = data[7:]
  print("packet ",str(ID)," sequence ",str(SEQUENCE_NUMBER,'utf-8')," accepted")

  # validate checksum
  check = packet.Packet(HEADER, SEQUENCE_NUMBER, LENGTH, DATA).getCHECKSUM()
  if(check == CHECKSUM):
    # Cek apakah sudah paket terakhir atau belum

    DATA_FILE += DATA

    if(TYPE == packet.FIN):
      print("Making File......")
      TYPE_REPLY = "0011"
      fileName = "received_file" + str(ID)
      f = open(fileName, "wb")
      f.write(DATA_FILE)
      f.close()
      print("file ",fileName," received")
      DATA_FILE = b''
    else:
      TYPE_REPLY = "0010"

    # Make header
    str_header = TYPE_REPLY + format(format(ID, "04b"))
    HEADER_REPLY = int(str_header,2).to_bytes(1,"big")

    # Make packet
    PACKET_REPLY = packet.Packet(HEADER_REPLY, SEQUENCE_NUMBER, LENGTH, DATA).encode()
    receiver.sendto(PACKET_REPLY, addr)
  else:
    print("Packet is loss")
