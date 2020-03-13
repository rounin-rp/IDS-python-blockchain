import socket
import pickle
import select
import Blockchain
import sys
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
	def __init__(self):
		Thread.__init__(self)
		self.setDaemon(True)
	def run(self):
		global flag
		global ser
		blen = 0
		var = 0
		while True:
			if(blen == 0):
				message = pickle.loads(ser.recv(1024))
			else:
				message = pickle.loads(ser.recv(var+blen+2))
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
			elif message[0] == 3003:
				blen = message[1]
				var = message[2]
			elif message[0] == 3004:
				flag = True
				print("main chain......")
				print(f"{message[1]}")
				flag = False
			else:
				flag = False
	def quit(self):
			sys.exit()


if __name__ == '__main__':
	obj = RecieveMessages()
	obj.start()
	while  True:
		while flag:
			continue
		print("enter your choice ")
		print("1 to add a block ")
		print("2 to display the blockchain")
		print("3 to exit  ")
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
			flag = True
			data = [3002,1]
			ser.send(pickle.dumps(data))
			flag = False
		elif opt == 3:
			print("quitting")
			obj.quit()
			sys.exit()
		else:
			print(f"invalid choice {opt}")


