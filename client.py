#import socket library
import socket
import sys
import errno

#Set IP and Port Number of Server
IP="127.0.0.1"
PORT = 1234

"""Size of our buffer is 10,000,00,000 characters
long and we will send first size of our msg to 
server
"""
HEADER_LENGTH = 10

"""create a socket object from socket library  
    AF (Address Family ) & INET (Internet) IPv4
    Socket will commuicate with these type of addresses
    Sock Stream is for Stream of data of TCP   
"""
#Get username from client
my_username=input("Username:    ")


#Make a client socket
client_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

#Connect client to Server
client_socket.connect((IP,PORT))

#set recv method to non-block 
#it will return if client does not enter anything
client_socket.setblocking(False)


#encode  username and send
username=my_username.encode("utf-8")
#calculate header of username with 10 bytes left formatting 
username_header=f"{len(username):<{HEADER_LENGTH}}".encode("utf-8")

#Send encoded header & username  to server 
client_socket.send(username_header + username)


#Chat After Connection
while True:
    #message to be sent by client
    #print username of each client in front to look pretty :)
    message=input(f"{my_username} > ")
    
    if message:
        #encode message to send
        message=message.encode("utf-8")
        #calculate header
        message_header=f"{len(message):<{HEADER_LENGTH}}".encode("utf-8")
        #send to server
        client_socket.send(message_header + message)
       



    #receive messages of other clients 
    try:
    	while True:
	        username_header=client_socket.recv(HEADER_LENGTH)
	        if not len(username_header):
	            print("Connection Lost")
	            sys.exit()

	        #First username_header & username of client is send by server    
	        username_length=int(username_header.decode("utf-8").strip())
	        username=client_socket.recv(username_length).decode("utf-8")

	        #Then message_header & message_length is sent
	        message_header=client_socket.recv(HEADER_LENGTH)
	        message_length=int(message_header.decode("utf-8").strip())

	        message=client_socket.recv(message_length).decode("utf-8")

	        print(f"{username} >  {message}")


    except IOError as e:
        if e.errno!=errno.EAGAIN and e.errno !=errno.EWOULDBLOCK:
            print('Reading Error: {}'.format(str(e)))
            sys.exit()

        continue

    #If any other error happened
    except Exception as e:        
         print('Error'.format(str(e)))
         sys.exit()   


    