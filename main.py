
# tester notre code par le terminal 
from classes.blockchain import Blockchain

blockchain1 = Blockchain('coucou', None)
print(blockchain1.block.hash)
block2 = Blockchain('salut', blockchain1.block)
print(blockchain2.block.hash)



