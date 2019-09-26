import sys
import struct

# constant
MAX_DATA_SIZE = 32768 # 32kb
MAX_PACKET_SIZE = 32775
DATA = 0x0
ACK = 0x1
FIN = 0x2
FIN_ACK = 0x3

class Packet:
  def __init__(self, HEADER, SEQUENCE_NUMBER, LENGTH, DATA):
    self.HEADER = HEADER
    self.SEQUENCE_NUMBER = SEQUENCE_NUMBER
    self.LENGTH = LENGTH
    self.DATA = DATA
    self.CHECKSUM = Packet.makeChecksum(self)

  def getHEADER(self):
    return self.HEADER

  def getSEQUENCE_NUMBER(self):
    return self.SEQUENCE_NUMBER

  def getLENGTH(self):
    return self.LENGTH
  
  def getDATA(self):
    return self.DATA

  def getCHECKSUM(self):
    return self.CHECKSUM

  @staticmethod
  def makeChecksum(self):
    SUM = self.HEADER + self.SEQUENCE_NUMBER + self.LENGTH + self.DATA
    check = int.from_bytes(SUM[0:2],byteorder ='big')

    for i in range (2,len(SUM)-2,2) :
      NextCheck = int.from_bytes(SUM[i:i+2],byteorder='big')
      check = (check ^ NextCheck)

    check = format(check, "08b")
    CHECKSUM = int(check,2).to_bytes(2, "big")
    return(CHECKSUM)

  def encode(self):
    return self.HEADER + self.SEQUENCE_NUMBER + self.LENGTH + self.CHECKSUM + self.DATA



    
