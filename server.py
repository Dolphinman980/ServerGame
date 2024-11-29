import socket
import threading

host = '127.0.0.1'
port = 12345

clients = []
aliases = []

def broadcast(message):
    for client in clients:
        client.send(message)

def handleClient(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
            print(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            alias = aliases[index]
            broadcast(f"{alias} has left the chat.".encode('utf-8'))
            aliases.remove(alias)
            break

def receiveConnections():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()

    print("Server is running...")
    while True:
        client, address = server.accept()
        print(f"Connection from {address} established.")


        alias = client.recv(1024).decode('utf-8')
        aliases.append(alias)
        clients.append(client)

        print(f"Alias of the client is {alias}.")


        thread = threading.Thread(target=handleClient, args=(client,))
        thread.start()

receiveConnections()
