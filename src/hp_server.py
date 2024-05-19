import threading
import sys
import hp_protocols as protocols 
import hp_utils as utils 
import socket

if utils.boolParam(sys.argv, ['-h', '--help']):
    print(utils.serverHelpMessage())
    sys.exit(0)

delay = 2
ip = utils.param(sys.argv, ['-i', '--ip'], '127.0.0.1')
port = utils.param(sys.argv, ['-i', '--ip'], '13131')
max_buffsize = utils.param(sys.argv, ['-m', '--max-buff-size'], '4096')

try:
    port = int(port)
except:
    port = 13131

try:
    max_buffsize = int(max_buffsize)
except:
    max_buffsize = 4096

ssocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ssocket.bind((ip, port))
ssocket.settimeout(delay)

print('(server): bound to ' + str(ip) + ':' + str(port))

peerBuff = []

while True:
    try:
        message, addr = ssocket.recvfrom(max_buffsize)
        if message.decode('utf-8') == 'CONNECT':
            if not peerBuff:
                peerBuff.append(addr)
            else:
                ssocket.sendto(('CONFIRM '+addr[0]+':'+str(addr[1])).encode('utf-8'), peerBuff[0])
                ssocket.sendto(('CONFIRM '+peerBuff[0][0]+':'+str(peerBuff[0][1])).encode('utf-8'), addr)
                peerBuff.pop()
    except socket.timeout as err:
        pass
ssocket.close()
