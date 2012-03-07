from websocket import *

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

socket = WebSocket('ws://localhost:5000', onmessage=my_msg_handler)
# socket.onopen = lambda: socket.send(encode_for_socketio('Hello world!'))
socket.onopen = lambda: socket.send('Hello world!')


# ws = websocket.create_connection('ws://localhost:5000/data')
# msg = "Hello, world!"
# msg = encode_for_socketio(msg)
# ws.send(msg)


try:
  asyncore.loop()
except KeyboardInterrupt:
  socket.close()
