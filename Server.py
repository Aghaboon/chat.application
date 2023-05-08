# Import required modules
import socket
import threading
from tkinter import *

# Server configuration
# socket.AF_INET, this case to use IPv4
# socket.SOCK_STREAM, this to use TCP socket
# socket.SOCK_DGRAM, this to use UDP socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = "192.168.56.1"
port = 14217

# method connects the socket to the specified host and port.
server.bind((host, port))

# method configures the server to accept up to 5 connections that are queued and listen for incoming connections.
server.listen(5)

# Create empty lists to hold client sockets and usernames
clients = []
usernames = []

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
            username = usernames[index]
            usernames.remove(username)
            broadcast(f"{username} left the chat!".encode("utf-8"))
            break

# Function to accept new client connections and start a new thread to handle each connection
def receive():
    while True:
        # Wait for a client connection, then accept it.
        client, addr = server.accept()
        print(f"Connected with {str(addr)}")

        # Ask client to send their username and add to lists of clients and usernames
        client.send("USER".encode("utf-8"))
        username = client.recv(1024).decode("utf-8")
        usernames.append(username)
        clients.append(client)

        # Broadcast to all clients that a new client has joined the chat
        print(f"Username of the client is {username}!")
        broadcast(f"{username} joined the chat!".encode("utf-8"))
        # client.send("Connected to the server!".encode("utf-8"))

        # Start a new thread to handle the client's connection
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


# Start the server and accept new connections
receive()

# -----------------------------------------------------------------
# for UDP
# def receive():
#     while True:
#         # Wait for a message from a client
#         message, client_address = server.recvfrom(1024)
#         username = message.decode("utf-8")
#
#         # Add the client to the list of clients and usernames
#         if client_address not in clients:
#             clients.append(client_address)
#             usernames.append(username)
#             print(f"Username of the client is {username}!")
#             broadcast(f"{username} joined the chat!".encode("utf-8"))
#
#         # Broadcast the message to all clients
#         broadcast(message)
