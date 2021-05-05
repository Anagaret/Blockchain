# tester notre code par le terminal 
from classes.blockchain import Blockchain

block1 = Blockchain('coucou', None)
print(block1.block.hash)
block2 = Blockchain('salut', block1.block)
print(block2.block.hash)



