import hashlib
import re
from datetime import datetime
import sqlite3
import json






class Block:
    def __init__(self, data, difficulty):
        last_block = self.get_last_block()
        if last_block is None:
            index = 0
            previous_hash = None
        else:
            print(last_block.data)
            index = last_block.index + 1
            previous_hash = last_block.get_previous_hash
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = 0
        self.timestamp = datetime.timestamp(datetime.now())
        self.index = index
        self.hash = self.create_hash_block(difficulty)
    
    def create_hash_block(self, difficulty):
        hash = self.create_hash()
        while not re.search(r"^[0]{"+ str(difficulty) + "}", hash):
                self.set_nonce(self.nonce + 1)
                hash = self.create_hash()
        return hash
    
    def create_hash(self):
        return  hashlib.sha256(str({ 'index': self.index, 'timestamp': self.timestamp, 'nonce': self.nonce, 'previous_hash': self.previous_hash, 'data': self.data}).encode('utf-8')).hexdigest()

    def set_hash(self, hash):
        self.hash = hash
    
    def set_nonce(self, nonce):
        self.nonce = nonce

    def get_last_block(self):
        connect = sqlite3.connect('./database.db')
        connect.row_factory = self.dict_factory
        try:
            sql = ''' SELECT * FROM block ORDER BY id DESC LIMIT 0, 1'''
            # connect.row_factory = self.dict_factory
            cursor = connect.cursor()
            return json.dumps(cursor.execute(sql).fetchone());
        except sqlite3.Error as er:
            raise ValueError("Erreur base de donnee")
    
    def dict_factory(self,cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d


  
    

