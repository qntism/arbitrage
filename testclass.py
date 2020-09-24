import requests, logging, json, os, time, sys
from web3 import Web3
sys.path.append("./classes")

from kyberpriceclass import kyberprice
from uniswappriceclass import uniswapprice

source = sys.argv[1]
destination = sys.argv[2]


amount = sys.argv[3]
kyberFirst = kyberprice.main(source, destination, amount)
uniswapFirst = uniswapprice.main(source, destination, amount)
print("kyber price ", str(kyberFirst))
print("uniswap price ", str(uniswapFirst))
#Need to calculate in liquidity provider fees and gas