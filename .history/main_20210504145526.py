
# tester notre code par le terminal 
from classes.blockchain import Blockchain

blockchain = Blockchain('coucou')
blockchain.add_block('salut')
print(len(blockchain.list_blocks))
block2 = blockchain.list_blocks[1]
print(block2.hash)


