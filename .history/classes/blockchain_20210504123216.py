from .block import Block
import hashlib
from datetime import datetime;


class Blockchain:
    def create_hash_and_nonce(block):
        print(block)
        # i = 0
        # expectedZero = 3
        # nonce = 1
        # hash = hashlib.new("sh256", data)
        # while (i < expectedZero):
        #     if (hash[i] == 0):
        #         i+=1
        #     else:
        #         nonce +=1
        #         i = 0
        #         hash = hashlib.new("sh256", data)
        # return  {'nonce' : nonce, 'hash': hash}
        
    def __init__(self, data, previous_block):
        if(previous_block is None):
            index = 0
            previous_hash = None
        else: 
            previous_hash = previous_block.hash
            index = previous_block.index + 1 
        timestamp = datetime.timestamp(datetime.now())


        self.block = Block(None, data, previous_hash, None, index, timestamp)
        obj_hash = create_hash_and_nonce(self.block)


    
            


            