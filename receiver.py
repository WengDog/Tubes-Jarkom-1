import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
addr = ("127.0.0.1", 5005)
sock.bind(addr)

while True:
  data,addr = sock.recvfrom(32768)
  print(data)
  print(int(data[1],2))