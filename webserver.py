from socket import *
import sys

# membuat tcp soket
serverSocket = socket(AF_INET, SOCK_STREAM)
serverPort = 8080 # nomor port
serverSocket.bind(('',serverPort)) # mengikat port ke soket
serverSocket.listen(1) #menunggu request
print("Ready to serve . . .")

while True:
    connectionSocket, addr = serverSocket.accept() # membuat soket koneksi dan menerima request

    try:
        #menerima message dan mencari file yang diminta
        message = connectionSocket.recv(1024).decode()
        filename = message.split()[1]
        f = open(filename[1:])
        outputdata = f.read()

        print("File found.")
        # membuat header bahwa file telah ditemukan
        headerLine = "HTTP/1.1 200 OK\r\n"
        connectionSocket.send(headerLine.encode())
        connectionSocket.send("\r\n".encode())

        # mengirim file ke klien
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.send("\r\n".encode())

        # memputuskan koneksi
        print("File sent.")
        connectionSocket.close()
    #jika error
    except IOError:

        # membuat header error 
        errHeader = "HTTP/1.1 404 Not Found\r\n"
        connectionSocket.send(errHeader.encode())
        connectionSocket.send("\r\n".encode())

        # mencari file error dan mengirim file error 
        ferr = open("notfound.html", 'r')
        outputerr = ferr.read()

        for i in range(0, len(outputerr)):
            connectionSocket.send(outputerr[i].encode())
        connectionSocket.send("\r\n".encode())

        #memputuskan koneksi
        print("Error message sent.")
        connectionSocket.close()

    # tutup aplikasi
    serverSocket.close()
    sys.exit()
