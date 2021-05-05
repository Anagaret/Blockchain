import hashlib
import re



class Block:
    def __init__(self, data, previous_hash,  index, timestamp):
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = 0
        self.timestamp = timestamp
        self.index = index
        self.hash = self.create_hash_block()
    
    def create_hash_block(self):
        hash = self.create_hash()
        # on passe le nonce à 1 car pour le hash du base64 d'une image cela est trop long 
        while not re.search(r"^[0]{1}", hash):
                self.set_nonce(self.nonce + 1)
                hash = self.create_hash()
        return hash
    
    def create_hash(self):
        return  hashlib.sha256(str({ 'index': self.index, 'timestamp': self.timestamp, 'nonce': self.nonce, 'previous_hash': self.previous_hash, 'data': self.data}).encode('utf-8')).hexdigest()

    def set_hash(self, hash):
        self.hash = hash
    
    def set_nonce(self, nonce):
        self.nonce = nonce

  
    

