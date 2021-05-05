from .blockchain import Blockchain
import base64
import os 
cwd = os.getcwd()


class PictureBlockchain(Blockchain):

    def __init__(self, path):
        data =  self.picture_to_base64(path)
        print(data)
        # Blockchain.__init__(data)
        
    
    def picture_to_base64(self, path):
        try:
            with open(cwd +'/pictures/' + path, 'rb') as picture_file:
                encoded_picture = base64.b64encode(picture_file.read())
            return encoded_picture
        except:
            raise ValueError('File path is wrong.')
    
    # def get_blockchain(self):
    #     retunr super().