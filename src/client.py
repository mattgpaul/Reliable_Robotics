# Client to use as an example of if we have a datastream coming from a system in a TCP/IP packet

import socket
from dataclasses import dataclass

@dataclass(frozen=True)
class DataClient:
    HEADER: int = 64
    PORT: int = 5050
    FORMAT: str = 'utf-8'
    DISCONNECT_MESSAGE: str = "!DISCONNECT"
    SERVER: str = "127.0.1.1"
    CLIENT = None
    
    if CLIENT is None:
        CLIENT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    CLIENT.connect((SERVER, PORT))

    def send(self, msg):
        message = msg.encode(self.FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(self.FORMAT)
        send_length += b' ' * (self.HEADER - len(send_length))
        self.CLIENT.send(send_length)
        self.CLIENT.send(message)