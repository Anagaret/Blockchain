import hashlib
import re
from datetime import datetime;




class Block:
    def __init__(self, data, difficulty):
        # self.data = data
        # self.previous_hash = previous_hash
        # self.nonce = 0
        # self.timestamp = timestamp = datetime.timestamp(datetime.now())
        # self.index = index
        # self.hash = self.create_hash_block(difficulty)
        get_previous_hash_bd()
    
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

    def get_previous_hash_bd():
        connect = sqlite3.connect('../database.db')
        try:
            sql = ''' SELECT * FROM block ORDER BY id DESC LIMIT 0, 1'''
            cursor = connect.cursor()
            last_block = cursor.execute(sql).fetchone()
        except sqlite3.Error as er:
            print(er)


  
    

