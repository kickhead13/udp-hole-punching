def clientCredentialsMessage():
    return 'CONNECT'.encode('utf-8')

def updateMessage():
    return 'UPDATE'.encode('utf-8')

def confirmMessage(ip, port):
    return ('CONFIRM ' + ip + ':' + 'port').encode('utf-8')

def peerCredentials(drecv):
    return drecv.decode('utf-8').split(' ')[1].split(':')
