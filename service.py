import socket
import json
import os
import time
import logging
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
import signal

class GracefulKiller:
  kill_now = False
  def __init__(self):
    signal.signal(signal.SIGINT, self.exit_gracefully)
    signal.signal(signal.SIGTERM, self.exit_gracefully)

  def exit_gracefully(self, signum, frame):
    self.kill_now = True
    log.info('PowerSync service is being stopped')

class Logger:
    def __init__(self):
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s', datefmt='%Z %Y:%m:%d %H:%M:%S')
        file_handler = RotatingFileHandler('./log/powersync.log', maxBytes=1024*1024*10, backupCount=10)
        file_handler.setFormatter(formatter)
        consoleHandler = logging.StreamHandler()
        consoleHandler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        self.logger.addHandler(consoleHandler)
    
    def debug(self,message):
        self.logger.debug(message)

    def info(self,message):
        self.logger.info(message)

    def warn(self,message):
        self.logger.warning(message)

    def error(self,message):
        self.logger.error(message)

    def crit(self,message):
        self.logger.critical(message)

def hamming_encode(data):
    data_bits = [int(bit) for bit in data]
    m = len(data_bits)
    r = 1

    while (2 ** r) < (m + r + 1):
        r += 1

    hamming_code = [0] * (m + r)
    j = 0
    for i in range(1, m + r + 1):
        if i == 2 ** j:
            j += 1
        else:
            hamming_code[i - 1] = data_bits.pop(0)

    for i in range(r):
        position = 2 ** i
        value = 0
        for j in range(1, m + r + 1):
            if j & position and j != position:
                value ^= hamming_code[j - 1]
        hamming_code[position - 1] = value

    return ''.join(map(str, hamming_code))

def hamming_decode(data):
    data_bits = [int(bit) for bit in data]
    m = len(data_bits)
    r = 0

    while (2 ** r) < m:
        r += 1

    error_pos = 0
    for i in range(r):
        position = 2 ** i
        value = 0
        for j in range(1, m + 1):
            if j & position:
                value ^= data_bits[j - 1]
        if value:
            error_pos += position

    if error_pos:
        data_bits[error_pos - 1] ^= 1

    decoded_data = []
    j = 0
    for i in range(1, m + 1):
        if i != 2 ** j:
            decoded_data.append(data_bits[i - 1])
        else:
            j += 1

    return ''.join(map(str, decoded_data))

def recv(port=51547):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', port))

    data, addr = sock.recvfrom(1024)
    encoded_message = data.decode('utf-8')
    decoded_message_bits = hamming_decode(encoded_message)
    decoded_message = ''.join(chr(int(decoded_message_bits[i:i+8], 2)) for i in range(0, len(decoded_message_bits), 8))
    
    return {"msg":decoded_message,"addr":addr}

killer = GracefulKiller()
log = Logger()
log.info('PowerSync service is starting')
log.info('PowerSync started successfully')

while not killer.kill_now:
    print(recv())
    hostname = "google.com" #example
    response = os.system("ping -c 1 " + hostname)

    #and then check the response...
    if response == 0:
        print(f"{hostname} is up!")
    else:
        print(f"{hostname} is down!")

log.info('PowerSync service stopped successfully')
