import socket
import pickle
import select
import Blockchain
from threading import *


IP = input('enter the ip : ')
PORT = int(input('enter the port : '))
username = input('enter the username : ')
ser = socket.socket()
ser.connect((IP,PORT))
first_message = [1001,username]
ser.send(pickle.dumps(first_message))
blockchain = Blockchain.Blockchain()
flag = False

class RecieveMessages(Thread):
	def run(self):
		global flag
		global ser
		while True:
			message = pickle.loads(ser.recv(1024))
			if message[0] == 2001:
				flag = True
				print(f"please validate the transaction below : ")
				print(f"{message[1]}")
				vote = input('\n do you think the above transaction is valid (y/n || 1/0) ?')
				vote = [2002,vote]
				ser.send(pickle.dumps(vote))
				flag = False
			elif message[0] == 2003 and message[1] == 1:
				print(f'congratulation the transaction is accepted !! ')
				data = blockchain.mine(message)
				print(f'mining successful!!')
				ser.send(pickle.dumps([3001,data]))
			else:
				flag = False


if __name__ == '__main__':
	obj = RecieveMessages()
	obj.start()
	while  True:
		while flag:
			continue
		print("enter your choice ")
		print("1 to add a block ")
		print("2 to delete a block ")
		try:
			opt = int(input())
		except:
			continue
		if(opt == 1):
			flag = True
			data = input('enter the data ')
			ser.send(pickle.dumps([2001,data]))
			flag = False
		elif opt == 2:
			pass
		else:
			print(f"invalid choice {opt}")


