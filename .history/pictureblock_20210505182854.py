from .block import Block
import base64
import os 
cwd = os.getcwd()


class PictureBlock(Block):

    def __init__(self, path):
        data =  self.picture_to_base64(path)
        Block.__init__(self, data,1)
        
    
    def picture_to_base64(self, path):
        try:
            with open(cwd +'/pictures/' + path, 'rb') as picture_file:
                encoded_picture = base64.b64encode(picture_file.read())
            return encoded_picture
        except:
            raise ValueError('File path is wrong.')
    

    # def add_picture(self, path):
