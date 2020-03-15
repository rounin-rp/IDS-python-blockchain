# IDS-python-blockchain

```
some@terminal python server.py
>>>enter the ip address : 127.0.0.1 (or any other ip adress)
>>>enter the port : 1234 (or any other port)
>>connection started at 127.0.0.1 1234

......................................................................

some@terminal python client.py
>>>enter the ip : 127.0.0.1 (same ip as the server)
>>>enter port : 1234 (1234)
>>>enter username : (any name)

.......then select the options.................

```

# Documentation

```
Every message sent over a socket is in the form of a list
The format of a message is : [id,message],
where 'id' is a unique identification of a message that tells the reciever what's the message is about, where 'message' is the actual message sent over. The 'message' could be of any type i.e. list,str,dict,tuple etc.

some examples of id
id = 2001, is used when a client is requesting for vote
id = 2002, is used when a client gives its vote
id = 2003, is used by the server to tell the client whether the transaction is accepted or rejected

Mining process:
After getting majority of votes in favour, the requesting miner will then use the consensus algorithm and mine the transaction onto the main chain on the server.

Blockchain :
All of the miners/users/clients can request the server to view the blockchain 
```
