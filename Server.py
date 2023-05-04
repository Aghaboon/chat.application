# Import required modules
import socket
import threading
from tkinter import *

# Server configuration

# socket.AF_INET, this case to use IPv4
# socket.SOCK_STREAM, this case to use TCP socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "127.17.18.1"
port = 14217

# method connects the socket to the specified host and port.
server.bind((host, port))

# method configures the server to accept up to 5 connections that are queued and listen for incoming connections.
server.listen(5)

# Create empty lists to hold client sockets and nicknames
clients = []
nicknames = []

# Function to broadcast message to all connected clients
def broadcast(message):
    for client in clients:
        client.send(message)

# Function to handle individual client connections
def handle(client):
    while True:
        try:
            # The 1024 represents the most data that can be received at once in bytes.
            message = client.recv(1024)
            # in this method, with the exception of the sender, everyone in the chat room receives the message.
            broadcast(message)
        except:
            # Remove the client from the list of clients if an error occurs, such as a disconnected client.
            index = clients.index(client)
            clients.remove(client)
            # Close client connection
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            broadcast(f"{nickname} left the chat!".encode("utf-8"))
            break

# Function to accept new client connections and start a new thread to handle each connection
def receive():
    while True:
        # Wait for a client connection, then accept it.
        client, addr = server.accept()
        print(f"Connected with {str(addr)}")

        # Ask client to send their nickname and add to lists of clients and nicknames
        client.send("NICK".encode("utf-8"))
        nickname = client.recv(1024).decode("utf-8")
        nicknames.append(nickname)
        clients.append(client)

        # Broadcast to all clients that a new client has joined the chat
        print(f"Nickname of the client is {nickname}!")
        broadcast(f"{nickname} joined the chat!".encode("utf-8"))
        client.send("Connected to the server!".encode("utf-8"))

        # Start a new thread to handle the client's connection
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

# Start the server and accept new connections
receive()