import threading
import socket
import time

# Define constants
PORT = 10000
SERVER = "localhost"
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"
JOIN_MSG = "!JOINED"
BYTE_SIZE = 1024

# Create our server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

# Holds the clients
clients = set()



def handle_client(conn, addr):
    try:
        connected = True 
        # Recive username
        username = conn.recv(BYTE_SIZE).decode(FORMAT)
        print(f"SERVER: {username} has joined the chat!")
        while connected:
            # Receive message
            msg = conn.recv(BYTE_SIZE).decode(FORMAT)

            if msg == JOIN_MSG:
                localTime1 = time.localtime()
                join_time = time.strftime("%I:%M:%S %p", localTime1)
                for c in clients:
                    c.send(f"{username} has joined the chat at {join_time}".encode(FORMAT))
            else:

                # Print message onto server
                print(f"{username}: {msg}")

                # Send message to all clients
                for c in clients:
                    if c is not conn:
                        c.send(f"{username}: {msg}".encode(FORMAT))
    except:
        print(f"SERVER: {username} has left")
        # Send to other users that the user has left the chat
        localTime2 = time.localtime()
        quit_time = time.strftime("%I:%M:%S %p", localTime2)
        for c in clients:
            if c is not conn:
                c.send(f"{username} has left the chat at {quit_time}".encode(FORMAT))
          
    finally:
        # Remove connection
        clients.remove(conn)
        conn.close()

def start():
    server.listen()
    print(f"[SERVER {SERVER} HAS CONNECTED]")
    while True:
        conn, addr = server.accept() # accept incoming connections
        clients.add(conn)
        thread = threading.Thread(target=handle_client, args=(conn,addr))
        thread.start()

if __name__ == '__main__':
    start()
