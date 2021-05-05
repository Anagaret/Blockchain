# tester notre code par le terminal 
from classes.blockchain import Blockchain

test = Blockchain('coucou', None)

print(str(test.block.hash))