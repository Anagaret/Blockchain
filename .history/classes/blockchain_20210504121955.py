from .block import Block
import hashlib

class Blockchain:
    def __init__(self, data, previous_block):
        if(previous_block is None):
            index = 0
            previous_hash = None
        previous_hash = previous_block.hash
        index = previous_block.index + 1 
        timestamp = datetime.timestamp(now)

        # obj_hash = create_hash_and_nonce({'index': index, 'previous_hash': previous_hash, "timestamp"})

        self.block = Block(hash, data, previous_hash, nounce, index)


    def create_hash_and_nonce(bloc):
        i = 0
        expectedZero = 3
        nonce = 1
        hash = hashlib.new("sh256", data)
        while (i < expectedZero):
            if (hash[i] == 0):
                i+=1
            else:
                nonce +=1
                i = 0
                hash = hashlib.new("sh256", data)
        return  {'nonce' : nonce, 'hash': hash}
            


            