
def param(argVec, paramLabels, default):
    for index, arg in enumerate(argVec[1:]):
        if argVec[index] in paramLabels:
            return arg 
    return default

def boolParam(argVec, paramLabels):
    for arg in argVec[1:]:
        if arg in paramLabels:
            return True
    return False

def handleClientInput(csocket, peerip, peerport, username):
    while True:
        try: 
            msg = input()
            if msg:
                csocket.send((username+': '+msg).encode('utf-8'))
        except:
            break
    csocket.close()

def clientHelpMessage():
    return """Usage: python hp_client.py [OPTIONS]
Instantiates UDP Hole Punching client.

OPTIONS:
  -i, --ip <IP>             set the I.P. address of the UHP
                            central server
  -p, --port <PORT>         set the port of the UHP central 
                            server app
  -m, --max-buff-size <M>   the maximum number of bytes that
                            can be recieved by client
  -u, --username <UN>       username to be displayed along
                            -side your messages
  -d, --delay <D>           amount of seconds before timeout
  -h, --help                display this message
    """


def serverHelpMessage():
    return """Usage: python hp_server.py [OPTIONS]
Instantiates UDP Hole Punching server.

OPTIONS:
  -i, --ip <IP>             set the I.P. address to which the
                            central server should be bound
  -p, --port <PORT>         set the port to which the server 
                            should be bound
  -m, --max-buff-size <M>   the maximum number of bytes that
                            can be recieved by server
  -h, --help                display this message
    """
