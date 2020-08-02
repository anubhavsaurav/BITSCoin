#Please note that hashlib library needs to be installed to be able to run this... 
#The blocks are stored in JSON Format.
import hashlib
import time
 
from binascii import hexlify


#Block class is used to create blocks. Blocks are then added to the blockchain.
class Block:
    def __init__(self, index, difficulty, nonce, previousHash, timestamp, currentHash,transaction):
        self.index = index
        self.difficulty = difficulty
        self.nonce = nonce
        self.previousHash = previousHash
        self.timestamp = timestamp
        # self.data = data
        self.currentHash = currentHash
        self.transaction=transaction
 
 
#Used to create the genesis block(the first blockof the blockchain) and verify following blocks.
def getGenesisBlock():
    s='0'
    r='0'
    a=0
    d={
        'sender':s,
        'reciever':r,
        'amount':0
    }
    return Block(0, 0, 0, '0', '1496518102.896031', '0q23nfa0se8fhPH234hnjldapjfasdfansdf23',d)
 
#Creates the 'chain' with the genesis block.
blockchain = [getGenesisBlock()]
 
#Calculates the hash of the block contents.
def calculateHash(index, difficulty, nonce, previousHash, timestamp, transaction):
    value = str(index) + str(difficulty) + str(nonce) + str(previousHash) + str(timestamp)
    sha = hashlib.sha256(value.encode('utf-8'))
    return str(sha.hexdigest())


#Produces a proof of work. 
def mineBlock(index, difficulty, nonce, previousHash, timestamp, transaction):
    print("Mining new block...")
 
    difficultyString = "" + ("0" * difficulty)
 
    while (True):
        value = str(index) + str(difficulty) + str(nonce) + str(previousHash) + str(timestamp)
 
        sha = hashlib.sha256(value.encode('utf-8'))
 
        checkStr = str(sha.hexdigest())[:difficulty]
 
        if (checkStr == difficultyString) or (difficulty == 0):
            print("Found hash: " + str(sha.hexdigest()))
            return Block(index, difficulty, nonce, previousHash, timestamp, str(sha.hexdigest()),transaction)
        else:
            nonce += 1
        str(sha.hexdigest())


def transactBlock(index,difficulty,nonce,previousHash,timestamp,transaction):
    # proof=0
    # previousBlock=getLatestBlock()
 
    while(True):
    	# print(nonce)
    	value=str(index)+str(getLatestBlock().difficulty)+str(nonce)+str(previousHash)+str(timestamp)
    	sha=hashlib.sha256(value.encode('utf-8'))
    	checkStr = str(sha.hexdigest())[:4]
 
    	if(checkStr == "0000"):
    		# print(nonce)
    		return Block(index,difficulty,nonce,previousHash,timestamp,str(sha.hexdigest()),transaction)
    	else:
    		nonce+=1
    	str(sha.hexdigest())
        
 
def calculateHashForBlock(block):
    return calculateHash(block.index, block.difficulty, block.nonce, block.previousHash, block.timestamp, block.transaction)
 
 
def getLatestBlock():
    return blockchain[-1]
 
 
def mineNextBlock(reciever,bal):
    previousBlock = getLatestBlock()
    nextIndex = previousBlock.index + 1
    nextDifficulty = previousBlock.difficulty
    nextTimestamp = str(time.time())
 
    blockTime = 0.5
    nextDifficulty += 1
    d={
        'sender':'0',
        'reciever':reciever,
        'amount':1
    }
 
    nextNonce = 0
    # print(nextDifficulty)
    createBlock = mineBlock(nextIndex, nextDifficulty, nextNonce, previousBlock.currentHash, nextTimestamp,d)
    bal[reciever]+=1
    return createBlock

#Checks the BITSCoin balance in the sender's wallet to see if the transaction is feasible
def transactionPossible(sender,amount,bal):
	if(bal[sender]<amount):
		return False
	else:
		return True

#Mandatory Function to verify Transactions. 
def verifyTransaction(sender,reciever,prevS,prevR,bal):
	block=getLatestBlock()
	if(block.transaction['sender']!=sender):
		return False
	if(block.transaction['reciever']!=reciever):
		return False
	amt=block.transaction['amount']
	if(prevS-amt!=bal[sender]):
		return False
	if(prevR+amt!=bal[reciever]):
		return False
 
	return True


 
def TransactNextBlock(sender,reciever,amount,bal):
    previousBlock=getLatestBlock()
    nextIndex=previousBlock.index+1
    nextDifficulty=0
    nextTimestamp=str(time.time())
    nextNonce=0
    d={
        'sender':sender,
        'reciever':reciever,
        'amount':amount
    }
    if(transactionPossible(sender,amount,bal)):
    	createBlock=transactBlock(nextIndex,nextDifficulty,nextNonce,previousBlock.currentHash,nextTimestamp,d)
    	bal[sender]-=amount
    	bal[reciever]+=amount
    	return createBlock
    else :
    	print("not possible. Account balance low")
 
def isSameBlock(block1, block2):
    if block1.index != block2.index:
        return False
    if block1.difficulty != block2.difficulty:
        return False
    if block1.nonce != block2.nonce:
        return False
    elif block1.previousHash != block2.previousHash:
        return False
    elif block1.timestamp != block2.timestamp:
        return False
    elif block1.transaction != block2.transaction:
        return False
    elif block1.currentHash != block2.currentHash:
        return False
    return True
 
#Add in check for time created
def isValidNewBlock(createBlock, previousBlock):
    if previousBlock.index + 1 != createBlock.index:
        print('Indices Do Not Match Up')
        return False
    elif previousBlock.currentHash != createBlock.previousHash:
        print("Previous hash does not match")
        return False
    elif calculateHashForBlock(createBlock) != createBlock.currentHash:
        print("Hash is invalid")
        return False
    return True
 
#Validates chain. Checks through each block in the chain to make sure they are all valid.
def isValidChain(bcToValidate):
    if not isSameBlock(bcToValidate[0], getGenesisBlock()):
        print('Genesis Block Incorrect')
        return False
 
    tempBlocks = [bcToValidate[0]]
    for i in range(1, len(bcToValidate)):
        if isValidNewBlock(bcToValidate[i], tempBlocks[i - 1]):
            tempBlocks.append(bcToValidate[i])
        else:
            return False
    return True
 
#Mandatory Function that lists all transactions made by the user. 
def viewUser(blockchain,username):
	for block in blockchain:
		if(block.transaction['sender']==username):
			print(str(block.transaction['amount']) +"rs sent to "+block.transaction['reciever'])
		if(block.transaction['reciever']==username):
			print(str(block.transaction['amount']) +"rs recieved from "+block.transaction['sender'])
 
 
def main():
	inp=0
	bal={}
	bal['harshit']=10000
	bal['anubhav']=10000
	bal['nilesh']=10000
	while(True):
		inp =int(input("1 for mine, 2 for user views, 3 for transaction, 4 for exit"))
		username=input("username ")
		if(inp==4):
			break;
		elif(inp==3):
			reciever=input("reciever ")
			amount=int(input("amount "))
			prevS=bal[username]
			prevR=bal[reciever]
			if(transactionPossible(username,amount,bal)):
				blockchain.append(TransactNextBlock(username,reciever,amount,bal))
				print(len(blockchain))
				if(verifyTransaction(username,reciever,prevS,prevR,bal)==False):
					print("transaction unsuccesful due to internal problem")
					bal[sender]=prevS
					bal[reciever]=prevR
					blockchain.pop()
				print(reciever+" balance ",bal[reciever])
				print(username+" balance ",bal[username])
			else:
				print("transaction not possible balance low")
 
		elif(inp==1):
			if(isValidChain(blockchain)):
				print("difficulty: ",getLatestBlock().difficulty+1)
				print("Previous Hash: ", getLatestBlock().currentHash)
				blockchain.append(mineNextBlock(username,bal))
				print(username+" balance "+str(bal[username]))
		elif(inp==2):
			viewUser(blockchain,username)
 
 
 
if __name__ == "__main__":
    main()