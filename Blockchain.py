import hashlib
import json
import randomString

class Blockchain:
    def __init__(self):
        self.Blockchain = self._loadBlockchain()
        self._tempchain = self._getBlock()
        self._nonceList = self._getNonces()
        self._block = {}
    
    def _getBlock(self):
        block = {
            'prev_hash' : '',
            'nonce' : '',
            'data' : [],
            'hash' : '' 
        }
        return block
    
    def _getEmptyList(self):
        temp = []
        return temp

    def _getPreviousBlock(self):
        if len(self.Blockchain) < 1:
            return None
        else:
            return self.Blockchain[-1]
    
    def append(self,data):
        self._tempchain['data'].append(data)

    
    def mine(self,data):
        print("reaching here......")
        if len(data) < 1:
            print('There is nothing to mine!!')
        else:
            print("reaching also here .....")
            block = self._getBlock()
            block['data'] = data[2][1]
            block['prev_hash'] = data[2][0]
            count = 0
            while True:
                print(count)
                count+=1
                nonce = randomString.getRandomString()
                block['nonce'] = nonce
                block['hash'] = hashlib.sha256(json.dumps(block).encode()).hexdigest()
                if block['hash'][0:4] == '0000':
                    break
            #self.Blockchain.append(block)
        #self._tempchain = self._getBlock()
        #self._saveBlockchain()
        print('reaching before return ')
        return block

    def mineChain(self,block):
        self.Blockchain.append(block)
        self._saveBlockchain()


    def _saveBlockchain(self):
        with open('.blockchain.txt',mode = 'w') as f:
            f.write(json.dumps(self.Blockchain))
            f.close()
    
    def _loadBlockchain(self):
        blockchain = []
        try:
            with open('.blockchain.txt',mode = 'r') as f:
                content = f.readline()
                if content:
                    blockchain = json.loads(content)
                f.close()
            if self._verifyBlockchain(blockchain = blockchain) == False:
                print("Blockchain is invalid!!!")
        except:
            blockchain.append(self._getGenesisBlock())
        return blockchain
    
    def _getNonces(self):
        List = []
        for block in self.Blockchain:
            List.append(block['nonce'])
        return List

    def _verifyBlockchain(self, blockchain ):
        temp = blockchain
        for i in range(len(temp)):
            if i == 0:
                temp[i]['hash'] = '0'*64
            else:
                temp[i]['hash'] = ''
                temp[i]['hash'] = hashlib.sha256(json.dumps(temp[i]).encode()).hexdigest()
                if temp[i]['prev_hash'] != temp[i-1]['hash']:
                    return False
        return True

    def _getGenesisBlock(self):
        genesisBlock = {
            'prev_hash' : None,
            'nonce' : None,
            'data' : None,
            'hash' : '0'*64
            }
        return genesisBlock
