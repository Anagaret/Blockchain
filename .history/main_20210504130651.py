# tester notre code par le terminal 
from classes.blockchain import Blockchain

block1 = Blockchain('coucou', None)
block2 = Blockchain('salut', block1)


# print(str(test.block.hash))