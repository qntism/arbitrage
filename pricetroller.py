import requests, logging, json, os, time, sys
from web3 import Web3
sys.path.append("./classes")

from kyberpriceclass import kyberprice
from uniswappriceclass import uniswapprice

ethprovider_url = 'https://mainnet.infura.io/v3/4766db13619a4175aa7cf834d3eeae42' # infura project ID
baseaccount = Web3.toChecksumAddress('0x2e9f3eb1e287b1081f4bc8ef5adbb80f063ae19e') # pubkey

def main():
	while True:
		source = sys.argv[1]
		destination = sys.argv[2]
		amount = sys.argv[3]
		kyber = kyberprice.main(source, destination, amount)
		uniswap = uniswapprice.main(source, destination, amount)

		kybercheck = float(kyberprice.main(source, destination, (float(uniswap))))
		uniswapcheck = float(uniswapprice.main(source, destination, (float(kyber))))
		
		text1 = "selling " + str(amount) + " " + source +  " on kyber gets " + str(kyber) + " " + destination
		text2 = "selling " + str(amount) + " " + source +  " on uniswap gets " + str(uniswap) + " " + destination
		text3 = "selling " + str(kyber) + " " + destination +  " on uniswap gets " + str(uniswapcheck) + " " + source	
		text4 = "selling " + str(uniswap) + " " + destination +  " on kyber gets " + str(kybercheck) + " " + source
		
		kyberarbitrage = "False"
		uniswaparbitrage = "False"
		if kybercheck > float(amount):
			kyberarbitrage = "True"
		if uniswapcheck > float(amount):
			uniswaparbitrage = "True"
			
		#text5 = "is " + str(uniswapcheck) + " greater than " + str(amount) + "? " + kyberarbitrage
		#text6 = "is " + str(kybercheck) + " greater than " + str(amount) + "? " + uniswaparbitrage
		
		print(text1)
		print(text2)
		print(text3)
		print(text4)	
		#print(text5)
		#print(text6)
		
		#if uniswaparbitrage == "True" or kyberarbitrage  == "True":
		break

if __name__ == '__main__':
    main()
#Need to calculate in liquidity provider fees and gas