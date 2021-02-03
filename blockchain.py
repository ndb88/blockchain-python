import datetime 
import hashlib 
import json 

from flask import Flask, jsonify 
  
  
class Blockchain: 
    
    ## Create first block, hash=0
    def __init__(self): 
        self.chain = [] 
        self.create_block(proof=1, previous_hash='0') 
  
    ## To create subsequent blocks
    def create_block(self, proof, previous_hash): 
        block = {'index': len(self.chain) + 1, 
                 'timestamp': str(datetime.datetime.now()), 
                 'proof': proof, 
                 'previous_hash': previous_hash} 
        self.chain.append(block) 
        return block 
        
    ## To show previous block
    def print_previous_block(self): 
        return self.chain[-1] 
        
    ## Proof of work function (sha256)
    def work_proof(self, previous_proof): 
        new_proof = 1
        check_proof = False
          
        while check_proof is False: 
            hash_operation = hashlib.sha256( 
                str(new_proof**2 - previous_proof**2).encode()).hexdigest() 
            if hash_operation[:4] == '00000': 
                check_proof = True
            else: 
                new_proof = new_proof + 1
                  
        return new_proof 
  
    def hash(self, block): 
        encoded_block = json.dumps(block, sort_keys=True).encode() 
        return hashlib.sha256(encoded_block).hexdigest() 
  
    def valid_chain(self, chain): 
        previous_block = chain[0] 
        block_index = 1
          
        while block_index < len(chain): 
            block = chain[block_index] 
            if block['previous_hash'] != self.hash(previous_block): 
                return False
                
            previous_proof = previous_block['proof'] 
            proof = block['proof'] 
            hash_operation = hashlib.sha256( 
                str(proof**2 - previous_proof**2).encode()).hexdigest() 
              
            if hash_operation[:4] != '00000': 
                return False
            previous_block = block 
            block_index = block_index + 1
          
        return True
  
  
## Creating the Web App
app = Flask(__name__) 
  
## Create new blockchain object
blockchain = Blockchain() 
  
## Mining a new block in the blockchain
@app.route('/mine_block', methods=['GET']) 

def mine_block(): 
    previous_block = blockchain.print_previous_block() 
    previous_proof = previous_block['proof'] 
    proof = blockchain.work_proof(previous_proof) 
    previous_hash = blockchain.hash(previous_block) 
    block = blockchain.create_block(proof, previous_hash) 
      
    response = {'message': 'A block has been mined!', 
                'index': block['index'], 
                'timestamp': block['timestamp'], 
                'proof': block['proof'], 
                'previous_hash': block['previous_hash']} 
      
    return jsonify(response), 200
  
## Show blockchain using JSON
@app.route('/get_chain', methods=['GET']) 
def show_chain(): 
    response = {'chain': blockchain.chain, 
                'length': len(blockchain.chain)} 
    return jsonify(response), 200
  
## Check blockchain validity
@app.route('/valid', methods=['GET']) 
def valid(): 
    valid = blockchain.valid_chain(blockchain.chain) 
      
    if valid: 
        response = {'message': 'Valid Blockchain.'} 
    else: 
        response = {'message': 'Invalid Blockchain.'} 
    return jsonify(response), 200
  
app.run(host='127.0.0.1', port=5000) 