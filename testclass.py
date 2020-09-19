import requests, logging, json, os, time, sys
from web3 import Web3
sys.path.append("./classes")

from kyberpriceclass import kyberprice
from uniswappriceclass import uniswapprice

source = "dai" # sys.argv[1]
destination = "usdc" # sys.argv[2]


amount = 100
 # sys.argv[3]
kyberFirst = kyberprice.main(source, destination, amount)
uniswapFirst = uniswapprice.main(source, destination, amount)
print("kyber price ", str(kyberFirst))
print("uniswap price ", str(uniswapFirst))
