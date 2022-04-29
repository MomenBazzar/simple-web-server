import socket #To include Python’s socket library

PORT = 6500 #Declaring unused port
SERVER = 'localhost' #Giving our server an ip address
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Create a welcoming socket
server.bind(ADDR)


def start(): #Declaring the function start
    server.listen() #To listen and wait for incoming requests
    print(f"[LISTENING] Server is listening on {SERVER}") #Printing on terminal
    while True:
        conn, addr = server.accept()
        msg = conn.recv(2048).decode(FORMAT)
        print(msg)
        ip = addr[0]
        port = addr[1]
        try:
            string_list = msg.split(' ')  # Split request from spaces
            requestFile = string_list[1]
            conn.send(f"HTTP/1.1 200 OK\r\n".encode())
            myfile = requestFile.split('?')[0]  # After the "?" symbol not relevent here
            myfile = myfile.lstrip('/')

            if myfile == '': #If nothing was send with the request, the default is the main html file
                myfile = 'index.html'
            elif myfile.lower() == 'sortbyname' or myfile.lower() == 'sortbyprice':
                # if the request is sort by name or price we do the sort and save the result into new file

                old_myfile = myfile
                myfile = 'items.txt'
                with open('input.txt', 'r+') as file, open(myfile, 'w') as outfile: #It will deal with input file as an input file, and items file as an output file
                    arr = []
                    for line in file:
                        name, price = line.replace('\n', '').split(';;') #It will put the first information before ;; inside the <name> variable and the data after ;; will be the price
                        arr.append([name, price]) #To create array of names and prices
                    if old_myfile.lower() == 'sortbyname':
                        arr.sort(key=lambda x: str(x[0])) #We used lambda function which helps us compare based on the names located at index 0 of the columns <before ;;>
                    else:
                        arr.sort(key=lambda x: int(x[1])) #Using lambda function to compare based on the prices located at index 1 of the columns <after ;;>
                    for data in arr:
                        #For loop to print the sorted data into a new file <items.txt>
                        outfile.write(f'{data[0]};;{data[1]}\n')

            requestFile = open(myfile, 'rb')
            response = requestFile.read()
            requestFile.close()
            #To check the requested order and send the appropriate data
            if myfile.endswith(".jpg"):
                conn.send(f"Content-Type: image/jpeg \r\n".encode(FORMAT))
            elif myfile.endswith(".png"):
                conn.send(f"Content-Type: image/png \r\n".encode(FORMAT))
            elif myfile.endswith(".css"):
                conn.send(f"Content-Type: text/css \r\n".encode(FORMAT))
            elif myfile.endswith(".txt"):
                conn.send(f"Content-Type: text/plain \r\n".encode(FORMAT))
            else:
                conn.send(f"Content-Type: text/html \r\n".encode(FORMAT))

        except Exception: #The exception that will be sent if the requested order was not found
            conn.send(f"Content-Type: text/html \r\n".encode(FORMAT)) 
            #HTML code for a simple page with the 404 error
            response = ('<html><title>Error 404</title><body><center><h1 style="color:red">The file is not found </h1> <hr> <p style= '
                        '"font-weight: bold;"> Momen Bazzar - 1192214 </p> <p style="font-weight: bold;"> '
                        'Mohammad Buirat - 1192896 </p> <p style= "font-weight: bold;"> Mohammad AbuJaber - 1190298 '
                        '</p> <hr> <h2> IP: ' + str(ip) + ', Port: ' + str(port)
                        + '</h2></center></body></html>').encode(FORMAT)
        conn.send(f"\r\n".encode())
        # Swnding the response to the user
        conn.send(response)
        conn.close()


print("[STARTING] server is starting...")
start()
