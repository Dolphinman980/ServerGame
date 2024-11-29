import socket
import threading
import pygame

id = int(input("Choose an ID: "))
host = '127.0.0.1'
port = 12345

screenWidth = 1920
screenHeight = 1080
screen = pygame.display.set_mode([screenWidth, screenHeight])
clock = pygame.time.Clock()
squarePositions = {
    
}

def receiveMessages(client):
    while True:

        messageReceived = client.recv(1024).decode('utf-8')
        print(messageReceived)
        squareID, squareX, squareY = messageReceived.split("|")
        squarePos = (int(squareX), int(squareY))

        squarePositions[squareID] = squarePos

        print(f"ID: {squareID} | Position: {squarePos}")



def sendMessages(client):
    while True:
        pygame.time.delay(100)
        mousePos = pygame.mouse.get_pos()
        message = f"{id}|{mousePos[0]}|{mousePos[1]}".encode()
        client.send(message)
        message = ""


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))
client.send(str(id).encode())

threadReceive = threading.Thread(target=receiveMessages, args=(client,))
threadReceive.start()

threadSend = threading.Thread(target=sendMessages, args=(client,))
threadSend.start()

running = True
while running:
    screen.fill([0, 0, 0])
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    for key in squarePositions:
        print(key)
        pygame.draw.circle(screen, [255, 255, 0], squarePositions[key], 10)


    pygame.display.flip()
