import requests, logging, json, os, time, sys
from web3 import Web3
sys.path.append("./classes")

from kyberpriceclass import kyberprice
from uniswappriceclass import uniswapprice

ethprovider_url = 'https://mainnet.infura.io/v3/4766db13619a4175aa7cf834d3eeae42' # infura project ID
baseaccount = Web3.toChecksumAddress('0x2e9f3eb1e287b1081f4bc8ef5adbb80f063ae19e') # pubkey

pairs = ["dai usdt"] 

def main():
	while True:
		source = "dai" # sys.argv[1]
		destination = "usdc" # sys.argv[2]
		amount = 10000 # sys.argv[3]
		kyber = kyberprice.main(source, destination, amount)
		uniswap = uniswapprice.main(source, destination, amount)

		kybercheck = kyberprice.main(source, destination, round(float(uniswap)))
		uniswapcheck = uniswapprice.main(source, destination, round(float(kyber)))
		
		text1 = "selling " + str(amount) + " " + source +  " on kyber gets " + str(kyber) + " " + destination
		text2 = "selling " + str(amount) + " " + source +  " on uniswap gets " + str(uniswap) + " " + destination
		text3 = "selling " + str(kyber) + " " + destination +  " on uniswap gets " + str(uniswapcheck) + " " + source	
		text4 = "selling " + str(uniswap) + " " + destination +  " on kyber gets " + str(kybercheck) + " " + source
		
		kyberarbitrage = "False"
		uniswaparbitrage = "False"
		if kybercheck < uniswap:
			kyberarbitrage = "True"
		if uniswapcheck < kyber:
			uniswaparbitrage = "True"
			
		text5 = "is " + uniswapcheck + " greater than " + str(amount) + "? " + kyberarbitrage
		text6 = "is " + kybercheck + " greater than " + str(amount) + "? " + uniswaparbitrage
		
		print(text1)
		print(text2)
		print(text3)
		print(text4)	
		print(text5)
		print(text6)
		
		if uniswaparbitrage == "True" or kyberarbitrage  == "True":
			break
		
		
	
if __name__ == '__main__':
    main()
