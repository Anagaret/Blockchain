from .block import Block
import hashlib
from datetime import datetime;
import re


class Blockchain:

    def __init__(self, data):
        self.list_blocks = []
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
        nonce = 0
        hash = hashlib.sha256(str({ 'index': index, 'timestamp': timestamp, 'nonce': nonce, 'previous_hash': previous_hash, 'data': data}).encode('utf-8')).hexdigest()
        while not re.search(r"^[0]{4}", hash):
                nonce +=1
                hash = hashlib.sha256(str({ 'index': index, 'timestamp': timestamp, 'nonce': nonce, 'previous_hash': previous_hash, 'data': data}).encode('utf-8')).hexdigest()
        self.list_blocks.append(Block(hash, data, previous_hash, nonce, index, timestamp))

    def validate_block(block):



            


            