# tester notre code par le terminal 
from classes.blockchain import Blockchain

block1 = Blockchain('coucou', None)
block2 = Blockchain('salut', block1.block)
print(block2)


# print(str(test.block.hash))