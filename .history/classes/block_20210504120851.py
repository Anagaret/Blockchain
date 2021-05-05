from datetime import datetime;

class Block:
    def __init__(self, hash, data, previous_hash, nonce, index, timestamp):
        self.hash = hash
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.timestamp = timestamp
        self.index = index


    def get_hash(self):
        return self.hash
    
    def set_hash(self, hash):
        self.hash = hash
    
    def get_data(self):
        return self.data
    
    def set_data(self, data):
        self.data = data

    def get_previous_hash(self):
        return self.previous_hash
    
    def set_previous_hash(self, previous_hash):
        self.previous_hash = previous_hash

    def get_nonce(nonce):
        return self.nonce
    
    def set_nonce(self, nonce):
        self.nounce = nonce

    def get_index(self):
        return self.index

    def get_timestamp(self):
        return self.timestamp

    def set_timestamp(timestamp):
        self.timestamp = timestamp

    # def set_index(self, index):
    #     self.index = index



    

