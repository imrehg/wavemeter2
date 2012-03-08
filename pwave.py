from websocket import *
import websocket, httplib

'''
connect to the socketio server
1. perform the HTTP handshake
2. open a websocket connection
'''
def connect(self) :
    conn  = httplib.HTTPConnection('localhost:8124')
    conn.request('POST','/socket.io/1/')
    resp  = conn.getresponse() 
    hskey = resp.read().split(':')[0]

    self._ws = websocket.WebSocket(
                    'ws://localhost:8124/socket.io/1/websocket/'+hskey,
                    onopen   = self._onopen,
                    onmessage = self._onmessage)

def my_msg_handler(msg):
  print 'Got "%s"!' % msg

def encode_for_socketio(message):
    """
    Encode 'message' string or dictionary to be able
    to be transported via a Python WebSocket client to 
    a Socket.IO server (which is capable of receiving 
    WebSocket communications). This method taken from 
    gevent-socketio.
    """
    MSG_FRAME = "~m~"
    HEARTBEAT_FRAME = "~h~"
    JSON_FRAME = "~j~"

    if isinstance(message, basestring):
            encoded_msg = message
    elif isinstance(message, (object, dict)):
            return encode_for_socketio(JSON_FRAME + json.dumps(message))
    else:
            raise ValueError("Can't encode message.")

    return MSG_FRAME + str(len(encoded_msg)) + MSG_FRAME + encoded_msg

# socket = websocket.WebSocket('ws://localhost:5000/', onmessage=my_msg_handler)

# self._ws = websocket.WebSocket(
#                     'ws://localhost:8124/socket.io/1/websocket/'+hskey,
#                     onopen   = self._onopen,
#                     onmessage = self._onmessage)

conn  = httplib.HTTPConnection('localhost:5000')
conn.request('POST','/socket.io/1/')
resp  = conn.getresponse() 
respdata = resp.read()
hskey = respdata.split(':')[0]
print respdata
print hskey
socket = websocket.WebSocket('ws://localhost:5000/socket.io/1/websocket/'+hskey, onmessage=my_msg_handler)
# # socket.onopen = lambda: socket.send(encode_for_socketio('Hello world!'))
senddata = '5:::{"message":"hi"}'
socket.onopen = lambda: socket.send(senddata)

# ws = websocket.create_connection('ws://localhost:5000/data')
# msg = "Hello, world!"
# msg = encode_for_socketio(msg)
# ws.send(msg)


try:
  asyncore.loop()
except KeyboardInterrupt:
  socket.close()
