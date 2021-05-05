
# tester notre code par le terminal 
from classes.blockchain import Blockchain
from classes.pictureblockchain import PictureBlockchain

blockchain = Blockchain('coucou')
print(blockchain.list_blocks[0].hash)
blockchain.add_block('salut')
print(len(blockchain.list_blocks))
block2 = blockchain.list_blocks[1]
print(block2.hash)
validate_block2 = blockchain.validate_block(block2)
print(validate_block2)

pictureblockchain = PictureBlockchain('test.jpg')
print(pictureblockchain.list_blocks[0].hash)

