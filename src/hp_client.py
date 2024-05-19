import sys
import socket
import time
import hp_utils as utils 
import hp_protocols as protocols
import threading

if utils.boolParam(sys.argv, ["-h", "--help"]):
    print(utils.clientHelpMessage())
    sys.exit(0)

ip = utils.param(sys.argv, ["-i", "--ip"], '127.0.0.1')
port = utils.param(sys.argv, ["-p", "--port"], '13131')
max_buffsize = utils.param(sys.argv, ["-m", "--max-buff-size"], '4096')
delay = utils.param(sys.argv, ["-d", "--delay"], '2')
username = utils.param(sys.argv, ['-u', '--username'], 'user')

try:
    delay = int(delay)
except:
    delay = 2

try:
    max_buffsize = int(max_buffsize)
except:
    max_buffsize = 4096

try: 
    port = int(port)
except:
    print("(error): port MUST be valid number > 1000", file=sys.stderr)
    sys.exit(1)

if __name__ == '__main__':
    csocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    csocket.connect((ip, port))
    csocket.send(protocols.clientCredentialsMessage())
    print('* SENT peer request')
    csocket.settimeout(delay)
    drecv = ''
    while drecv == '':
        try: 
            drecv = csocket.recv(max_buffsize)
        except socket.timeout as err:
            csocket.send(protocols.updateMessage())
            print('* SENT update notice')
    print('* RECIEVED [' + drecv.decode('utf-8') + '] from (' + ip + ':' + str(port) + ')')
    (peerip, peerport) = protocols.peerCredentials(drecv) 
    csocket.connect((peerip, int(peerport)))
    wthread = threading.Thread(target=utils.handleClientInput, args=[csocket, peerip, peerport, username], daemon=True)
    wthread.start()
    rcvmsg = ''
    while True:
        try: 
            rcvmsg = csocket.recv(max_buffsize)
            if rcvmsg and not rcvmsg.decode('utf-8').startswith('UPDATE'):
                print(rcvmsg.decode('utf-8'))
        except socket.timeout as err:
            pass
            #csocket.send(protocols.updateMessage())
        except: 
            break
csocket.close()
