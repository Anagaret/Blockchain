from .blockchain import Blockchain
import base64
import os 
dir_path = os.path.dirname(os.path.realpath(__file__))


class PictureBlockchain(Blockchain):

    def __init__(self, path):
        data =  self.picture_to_base64(path)
        Blockchain.__init__(data)
        
    
    def picture_to_base64(self, path):
        print(dir_path + '/pictures' + path)
        # try:
        #     with open(os.getcwdb() + '/pictures' + path, 'rb') as picture_file:
        #         encoded_picture = base64.b64encode(picture_file.read())
        #     return encoded_picture
        # except:
        #     raise ValueError('File path is wrong.')
    
    # def get_blockchain(self):
    #     retunr super().