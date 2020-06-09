#import socket module
import socket
#import select module for I/O monitoring functions
import select

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
server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

#bind IP and PORT To socket as tuple
server_socket.bind((IP, PORT))

#make the server listen request
server_socket.listen()

#store all sockets in a list including server_socket
sockets_list = [server_socket] 

"""make a client socket dictionary to store object of client socket
client will be the key and user data is value
It will store client username's
"""
clients={}

#make a method to recieve messages from diff. client
def receive_msg(client_socket):
    try:
        #We will recieve header first (This is an encoded string )
        message_header=client_socket.recv(HEADER_LENGTH)
        
        #If client closed the connection nothing received
        if not len(message_header):
            return False
        
        #calculate the length of msg received from client from message header string 
        # strip away extra spaces added by formatter  
        message_length=int(message_header.decode("utf-8").strip())

        """As we have got length of message (message_length) 
        being sent by client so will receive that much bytes
        in  Line 55 
        """

        #return a dictionary of username and message
        return {"header":message_header, "data" : client_socket.recv(message_length)}

    #If some client leaves the chat
    except:
        return False


#Making Server on forever
while True:
    """The arguments to select() are three lists 
    1.List of the objects to be checked for incoming data to be read
    2.The second contains objects that will receive outgoing data, 
    3.The third those that may have an error .
         Also select() returns three new lists 
    1.Sockets in the readable list have incoming data buffered and available to be read. 
    2.Sockets in the writable list have free space in their buffer and can be written to. 
    3.The sockets returned in exceptional have had an error      """ 
    read_sockets, write_sockets, exceptional_sockets = select.select(sockets_list, [], sockets_list)
    #for loop on read_sockets
    for i in read_sockets:
        #If new Connection then read_socket is server_socket
        if i==server_socket:
            
            """The return value is a pair (conn, address) where 
            conn is a new socket object usable to send and 
            receive data on the connection,and address is the address   
            bound to the socket on the other end of the connection."""
            client_socket, client_address= server_socket.accept()
            
            #store message recieved from client_socket 
            #recieve_msg is function returing dictionary
            user=receive_msg(client_socket)
            #first time joined and closed connection
            if user is False:
                continue

            #store this socket is list of sockets
            sockets_list.append(client_socket)

            #storing username of client
            clients[client_socket]=user
            
            print(f"Chat Joined By IP: {client_address[0]} Port:{client_address[1]} Username: {user['data'].decode('utf-8')}")
            
        else:
            message=receive_msg(i)

            if message is False:
                print(f"{clients[i]['data'].decode('utf-8')} has left the chat ")
                sockets_list.remove(i)
                del clients[i]
                continue

            user=clients[i]
            print(f"Recieved Message From {user['data'].decode('utf-8')}: {message['data'].decode('utf-8')}")

            #Share This Message To EveryBody except sender
            for client_socket in clients:
                if client_socket !=i:
                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])

    #If there is any exceptional socket
    for i in exceptional_sockets:
        sockets_list.remove(i)
        del clients[i]











