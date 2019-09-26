import sys
import struct

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
    CHECKSUM = struct.pack('h',check)
    return(CHECKSUM)

  def encode(self):
    PACKET = bytearray()
    PACKET.append(int.from_bytes(self.HEADER, byteorder="big"))
    PACKET.append(int.from_bytes(self.SEQUENCE_NUMBER, byteorder="big"))
    PACKET.append(int.from_bytes(self.LENGTH, byteorder="big"))
    PACKET.append(int.from_bytes(self.CHECKSUM, byteorder="big"))
    PACKET.append(int.from_bytes(self.DATA, byteorder="big"))

    return PACKET



    
