import socket
import threading
import pygame

id = int(input("Choose an ID: "))
host = '10.1.1.51'
port = 50000
HEADER = 64

squarePositions = {

}


def receiveMessages(client):
    while True:
        messageReceived = client.recv(1024).decode('utf-8')
        print(messageReceived)
        try:
            squareID, squareX, squareY = messageReceived.split("|")
            squarePos = (int(squareX), int(squareY))

            squarePositions[squareID] = squarePos

            print(f"ID: {squareID} | Position: {squarePos}")
        except:
            pass


def sendMessages(client):
    while True:
        pygame.time.delay(16)
        mousePos = pygame.mouse.get_pos()

        message = f"{id}|{mousePos[0]}|{mousePos[1]}".encode()
        messageLength = f"{len(message):<{HEADER}}".encode()  # Pad to 64 bytes
        try:
            client.send(messageLength)  # Send padded length
            client.send(message)  # Send the actual message
        except ConnectionError:
            print("Connection lost. Exiting...")
            break


def play():
    screenWidth = 1920
    screenHeight = 1080
    screen = pygame.display.set_mode([screenWidth, screenHeight])
    clock = pygame.time.Clock()
    running = True
    while running:
        pygame.time.delay(50)
        screen.fill([0, 0, 0])
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        for key in squarePositions:
            print(key)
            pygame.draw.circle(screen, [255, 255, 0], squarePositions[key], 10)

        pygame.display.flip()


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))
client.send(str(id).encode())

threadReceive = threading.Thread(target=receiveMessages, args=(client,))
threadReceive.start()

threadSend = threading.Thread(target=sendMessages, args=(client,))
threadSend.start()

threadPlay = threading.Thread(target=play, args=())
threadPlay.start()
