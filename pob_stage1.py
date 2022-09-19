import json
from http.client import NotConnected
from math import *
import random
from hashlib import sha256
class Block:
    def __init__(self,txn_data ,hash,merkleRoot = None,Nounce = None):
        self.txn_data = txn_data
        self.block_hash = hash
        self.merkleroot = merkleRoot
        self.Nounce = Nounce
        self.prev_hash = None
        self.prev_block = None
    def addToBlockChain(self,Block_chain) -> bool:
        self.pev_block = Block_chain.top_block
        self.prev_hash = Block_chain.top_block.block_hash
        Block_chain.top_block = self
        return True

class BlockChain:
    def __init__(self,top_block:Block):
        self.top_block = top_block

def hash(successful_transaction , nounce) ->str :
    a_string = json.dumps(successful_transaction)+str(nounce)
    hashed_string = sha256(a_string.encode('utf-8')).hexdigest()
    return hashed_string
def merkle_root(successful_transaction ) ->str :
    a_string = json.dumps(successful_transaction)
    hashed_string = sha256(a_string.encode('utf-8')).hexdigest()
    return hashed_string
def POB_Consensus() -> str:
    consensus_probability = []
    for pub_key in burn_proofs:
        consensus_probability += [pub_key]*burn_proofs[pub_key]
    miner_id = random.choice(consensus_probability)
    return miner_id

def mine(Mem_pool):
    print("\n\n\n --- Mining Started ....")
    miner_id = POB_Consensus()
    print("selected miner:",miner_id)
    #txns verfication
    # verify markel root
    # cal block hash
    difficulty_level = 4
    nounce =1
    Hash = None
    while(True):
        Hash= hash(Mem_pool ,nounce)
        nounce+=1
        if(Hash[0:difficulty_level]=="0"*difficulty_level):
            print("BLOCK CREATED ")
            break
    # Nounce = 87584593
    if(Hash is None):
        return False
    block = Block(txn_data = Mem_pool,
                    hash = Hash,
                    merkleRoot= merkle_root(Mem_pool),
                    Nounce = nounce-1)
    # broad cast the block to every node to add into their block_chain
    print('block created')
    block.addToBlockChain(Block_chain)
    print('block added to chain')
    print('Block chain --> \n\n')
    count = 5
    while(count > 0):
        block = Block_chain.top_block
        print(block.txn_data)
        block = block.prev_block
        count -= 1

def add_txn(data):
    limit = 2
    Mem_pool.append(data)
    if(len(Mem_pool == limit)):
        mine()
        Mem_pool = [] 
def transaction():
    sender_pubic_key=input("enter your public key : ")
    receiver_public_key = input("enter receiver public key : ")
    amount = int(input("enter amount : "))
 
    data = {"sender":sender_pubic_key, "receiver":receiver_public_key, "transaction_amount":amount}
    if(users.get(sender_pubic_key)!=None and users.get(receiver_public_key)!=None and users.get(sender_pubic_key)>=amount):
        print("successful")
        users[sender_pubic_key]=users.get(sender_pubic_key)-amount
        users[receiver_public_key]=users.get(receiver_public_key)+amount
        Mem_pool.append(data)
        # add_txn()
        print(Mem_pool)
    else:
        print("unsuccessful ")
        unsuccessful_transcation.append(data)
        print(unsuccessful_transcation)
 

users={
    "asd001":101,"asd005":105,"asd009":109,
    "asd002":102,"asd006":110,"asd001":110,
    "asd003":103,"asd007":111,"asd001":111,
    "asd004":104,"asd008":112,"asd001":112
}
burn_proofs={"asd001":20,"asd005":5,"asd009":19,
"asd002":12,"asd006":11,"asd001":10}

Mem_pool =[]
unsuccessful_transcation = []
Mem_pool = []
Genisis_block = Block("genisis",sha256("genisis".encode('utf-8')).hexdigest())
Block_chain = BlockChain(Genisis_block)
val =3
print(Block_chain.top_block.txn_data)
while(val!=2):
    print("do you want to perform a transaction if yes enter 1 else 2")
    try:
        val=int(input())
    except:
        print("Choose between 1 and 2 :")
        val = int(input())
    if(val==1):
        transaction()
        if(len(Mem_pool)==2):
          mine(Mem_pool)
          Mem_pool=[] 

