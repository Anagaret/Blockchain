
# tester notre code par le terminal 
from classes.blockchain import Blockchain

blockchain = Blockchain('coucou')
blockchain.add_block('salut')
print(len(blockchain.list_blocks))
blockchain.validate_block(blockchain.list_blocks[1])



