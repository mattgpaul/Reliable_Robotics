# Server example to demonstrate the user receiving data from a source

import socket
import threading
from dataclasses import dataclass

class DataServer:
    HEADER: int = 64
    PORT: int = 5050
    FORMAT = 'utf-8'
    DISCONNECT_MESSAGE = "!DISCONNECT"
    IP = None

    if IP is None:
        IP = socket.gethostbyname(socket.gethostname())
        
    print(IP)
    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.bind((IP, PORT))


    def handle_client(self, conn, addr):
        print(f'[NEW CONNECTION] {addr} connected')
        connected = True
        while connected:
            msg_length = conn.recv(self.HEADER).decode(self.FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(self.FORMAT)
                if msg == self.DISCONNECT_MESSAGE:
                    connected = False
                    
                print(f"[{addr}] {msg}")
            
        conn.close()
            

    def start(self):
        self.SERVER.listen()
        print(f"[LISTENING] Server is listening on {self.SERVER}")
        while True:
            conn, addr = self.SERVER.accept()
            thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

    print("[STARTING] server is starting...")



