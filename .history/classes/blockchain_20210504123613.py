from .block import Block
import hashlib
from datetime import datetime;


class Blockchain:

       

    def __init__(self, data, previous_block):
        if(previous_block is None):
            index = 0
            previous_hash = None
        else: 
            previous_hash = previous_block.hash
            index = previous_block.index + 1 
        timestamp = datetime.timestamp(datetime.now())

        i = 0
        expectedZero = 3
        nonce = 1
        data_hash = { 'index': index, 'timestamp': timestamp, 'nonce': nonce, 'previous_hash': previous_hash}
        hash = hashlib.new("sh256", data_hash)
        while (i < expectedZero):
            if (hash[i] == 0):
                i+=1
            else:
                nonce +=1
                i = 0
                hash = hashlib.new("sh256", data_hash)
        print(hash)
        print(nonce)

        self.block = Block(hash, data, previous_hash, nonce, index, timestamp)


            


            