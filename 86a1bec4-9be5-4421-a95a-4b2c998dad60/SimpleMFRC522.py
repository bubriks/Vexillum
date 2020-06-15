# Code by Simon Monk https://github.com/simonmonk/

import MFRC522
#import RPi.GPIO as GPIO
  
class SimpleMFRC522:

  READER = None
  
  KEY = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
  SECTOR = 7
  NUMOFSECTORS = 15
  
  def __init__(self):
    self.READER = MFRC522.MFRC522()
  
  def read(self):
      id, text = self.read_no_block()
      while not id:
          id, text = self.read_no_block()
      return id, text

  def read_id(self):
    id = self.read_id_no_block()
    while not id:
      id = self.read_id_no_block()
    return id

  def read_id_no_block(self):
      (status, TagType) = self.READER.MFRC522_Request(self.READER.PICC_REQIDL)
      if status != self.READER.MI_OK:
          return None
      (status, uid) = self.READER.MFRC522_Anticoll()
      if status != self.READER.MI_OK:
          return None
      return self.uid_to_num(uid)
  
  def read_no_block(self):
    (status, TagType) = self.READER.MFRC522_Request(self.READER.PICC_REQIDL)
    if status != self.READER.MI_OK:
        return None, None
    (status, uid) = self.READER.MFRC522_Anticoll()
    if status != self.READER.MI_OK:
        return None, None
    id = self.uid_to_num(uid)
    self.READER.MFRC522_SelectTag(uid)
    
    data = []
    text_read = ''
    for i in range(self.SECTOR, self.SECTOR + (4 * self.NUMOFSECTORS), 4):
        #print("sector key " + str(i))
        status = self.READER.MFRC522_Auth(self.READER.PICC_AUTHENT1A, i, self.KEY, uid)
        i = i - 4
        for x in range(3):
            i += 1
            #print("block " + str(i))
            if status == self.READER.MI_OK:
                block = self.READER.MFRC522_Read(i) 
                if block:
                    data += block
    if data:
        text_read = ''.join(chr(i) for i in data)

    self.READER.MFRC522_StopCrypto1()
    return id, text_read
    
  def write(self, text):
      id, text_in = self.write_no_block(text)
      while not id:
          id, text_in = self.write_no_block(text)
      return id, text_in

  def write_no_block(self, text):
      (status, TagType) = self.READER.MFRC522_Request(self.READER.PICC_REQIDL)
      if status != self.READER.MI_OK:
          return None, None
      (status, uid) = self.READER.MFRC522_Anticoll()
      if status != self.READER.MI_OK:
          return None, None
      id = self.uid_to_num(uid)
      self.READER.MFRC522_SelectTag(uid)
      
      data = bytearray()
      data.extend(bytearray(text.ljust(3 * self.NUMOFSECTORS * 16).encode('ascii')))
      y = 0
      for i in range(self.SECTOR, self.SECTOR + (4 * self.NUMOFSECTORS), 4):
        #print("sector key " + str(i))
        status = self.READER.MFRC522_Auth(self.READER.PICC_AUTHENT1A, i, self.KEY, uid)
        self.READER.MFRC522_Read(i)
        i = i - 4
        if status == self.READER.MI_OK:
            for x in range(3):
                i += 1
                #print("block " + str(i))
                self.READER.MFRC522_Write(i, data[(y*16):(y+1)*16])
                y += 1
      self.READER.MFRC522_StopCrypto1()
      return id, text[0:(3 * self.NUMOFSECTORS * 16)]
      
  def uid_to_num(self, uid):
      n = 0
      for i in range(0, 5):
          n = n * 256 + uid[i]
      return n
