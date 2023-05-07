# Import socket module
# Import sys to terminate the program
from socket import *
import sys

# Preparing the socket, tubes nomor 1
serverSocket = socket(AF_INET, SOCK_STREAM)
serverPort = 8080 # Arbitrary port number
serverSocket.bind(('',serverPort)) # Binding the port to the socket
serverSocket.listen(1) # Waiting for a request
print("Ready to serve . . .")

while True:
    connectionSocket, addr = serverSocket.accept() # Accepting request

    try:
        # Recieve message and check file name, tubes nomor 3
        message = connectionSocket.recv(1024).decode()
        filename = message.split()[1]
        f = open(filename[1:])
        outputdata = f.read()

        print("File found.")
        # Returns header line informing that the file was found, tubes nomor 4
        headerLine = "HTTP/1.1 200 OK\r\n"
        connectionSocket.send(headerLine.encode())
        connectionSocket.send("\r\n".encode())

        # Sends the file, tubes nomor 5
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.send("\r\n".encode())

        # Terminates the conection
        print("File sent.")
        connectionSocket.close()

    except IOError:
        print("Warning: file not found.")

        # Returns the error header to the browser
        errHeader = "HTTP/1.1 404 Not Found\r\n"
        connectionSocket.send(errHeader.encode())
        connectionSocket.send("\r\n".encode())

        # Opens and sends the error page to the browser
        ferr = open("notfound.html", 'r')
        outputerr = ferr.read()

        for i in range(0, len(outputerr)):
            connectionSocket.send(outputerr[i].encode())
        connectionSocket.send("\r\n".encode())

        # Terminates the connection
        print("Error message sent.")
        connectionSocket.close()

    # Closes the application
    serverSocket.close()
    sys.exit()
