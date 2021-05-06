from .block import Block

class PictureBlock(Block):

    def __init__(self, filename):
        data =  self.picture_to_base64(filename)
        Block.__init__(self, data,1)
        
    
    def picture_to_base64(self, filename):
        try:
            with open(cwd +'/pictures/' + filename, 'rb') as picture_file:
                encoded_picture = base64.b64encode(picture_file.read())
            return encoded_picture
        except:
            raise ValueError('Probleme convertion image en base 64.')