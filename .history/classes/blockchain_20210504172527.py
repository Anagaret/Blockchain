from .block import Block
from datetime import datetime;
import os 
cwd = os.getcwd()
import json


class Blockchain:

    def __init__(self, data, difficulty):
        self.list_blocks = []
        self.difficulty = difficulty
        self.add_block(data)

   

    def add_block(self, data):
        if(len(self.list_blocks) == 0):
            index = 0
            previous_hash = None
        else: 
            previous_block = self.list_blocks[-1]
            previous_hash = previous_block.hash
            index = previous_block.index + 1 
        timestamp = datetime.timestamp(datetime.now())
        self.list_blocks.append(Block(data, previous_hash, index, timestamp, self.difficulty))

    def validate_block(self, block):
        hash = Block(block.data, block.previous_hash, block.index, block.timestamp, self.difficulty).create_hash()
        return (hash == block.hash)
    
    def block_to_json(block):
        return {
                'index': block.index,
                'previous_hash': block.previous_hash,
                'timestamp': block.timestamp,
                'data': block.data,
                'hash': block.hash,
                'nonce': block.nonce
        }
    def store_json(self, filename):
        # with open(cwd +'/jsons/' + filename + '.json', 'w', encoding='utf-8') as json_file:
            

                # for block in self.list_blocks:
                #     block = {
                #         'index': block.index,
                #         'previous_hash': block.previous_hash,
                #         'timestamp': block.timestamp,
                #         'data': block.data,
                #         'hash': block.hash,
                #         'nonce': block.nonce
                #     }
                    
                #     json.dump(block, json_file, ensure_ascii=False, indent=4)
    result = map(self.block_to_json,self.list_blocks)
    print(list(result))
        # json_file.close()



    

   



            


            