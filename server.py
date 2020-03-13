import socket
import select
import pickle
import Blockchain

IP = input('enter the ip address : ')
PORT = int(input("enter the port : "))

server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

server_socket.bind((IP,PORT))
server_socket.listen()
print(f"connection started at {IP} {PORT}")
socket_list = [server_socket,]
clients = {}

total_miners = 0
votes = 0

block_length = 0
requesting_socket = ''
toMine = ''
total_voters = 0

def recieveMessages(client_socket):
    try:
        message = pickle.loads(client_socket.recv(1024))
        if not len(message):
            return False
        return message
    except:
        return False

while True:
    blockchain = Blockchain.Blockchain()
    readers,_,errors = select.select(socket_list,[],socket_list)
    votes = 0
    request = False
    for notified_socket in readers:
        if notified_socket == server_socket:
            client_socket,client_address = server_socket.accept()
            userinfo = recieveMessages(client_socket)
            if userinfo is False:
                continue
            socket_list.append(client_socket)
            clients[client_socket] = userinfo[1]
            total_miners = total_miners+1
            print(clients)
            print(f"accepted connection from {userinfo[1]} at {client_address}")
        else:
            message = recieveMessages(notified_socket)
            if message is False:
                print(f"disconnected from {clients[notified_socket]}")
                socket_list.remove(notified_socket)
                total_miners = total_miners-1
                del clients[notified_socket]
            else:
                if(message[0] == 2001):
                    print(f"{clients[notified_socket]} requesting vote ")
                    requesting_socket = notified_socket
                    for sockets in socket_list:
                        if(sockets == server_socket or sockets == notified_socket):
                            print("ha ")
                            continue
                        print(f"sent to {clients[sockets]}")
                        sockets.send(pickle.dumps(message))
                        toMine = message[1]
                elif(message[0] == 2002):
                    if(message[1] == 1 or message[1] == '1' or message[1] == 'y' or message[1] == 'Y'):
                        votes = votes + 1
                        request = True
                        total_voters+=1
                    else:
                        total_voters+=1
                elif(message[0] == 3001):
                    print("data got to mine ")
                    data = message[1]
                    blockchain.mineChain(data)
                elif(message[0] == 3002):
                    chain = blockchain.Blockchain
                    print(chain)
                    data = [3003,len(str(chain)),len(str(len(str(chain))))]
                    notified_socket.send(pickle.dumps(data))
                    notified_socket.send(pickle.dumps([3004,chain]))

    if(request and total_voters == total_miners-1):
        print(f"i am inside request total votes = {votes} and total miners = {total_miners-1}")
        if(votes/(total_miners-1) >= 0.5):
            prev_hash = blockchain.Blockchain[-1]['hash']
            requesting_socket.send(pickle.dumps([2003,1,[prev_hash,toMine]]))
            toMine = ''
        else:
            requesting_socket.send(pickle.dumps([2003,0]))
        request = False
        votes = 0
        total_voters = 0

    for notified_socket in errors:
        print(f"something is wrong with {clients[notified_socket][0]}")
        socket_list.remove(notified_socket)
        del clients[notified_socket]
    print("done circulation")