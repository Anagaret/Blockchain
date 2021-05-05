
# tester notre code par le terminal 
from classes.blockchain import Blockchain
from classes.pictureblockchain import PictureBlockchain

blockchain = Blockchain('coucou')
blockchain.add_block('salut')
print(len(blockchain.list_blocks))
block2 = blockchain.list_blocks[1]
validate_block2 = blockchain.validate_block(block2)
print(validate_block2)

pictureblockchain = PictureBlockchain('test.png')

