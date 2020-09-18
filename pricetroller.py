import requests, logging, json, os, time, sys
from web3 import Web3

tokens = json.load(open('abi/kyber_currencies.json', 'r'))["data"]
tokenarray = {}
for i in tokens: tokenarray[i["symbol"].lower()] = (Web3.toChecksumAddress(i["address"]), 10**i["decimals"])
#print(tokenarray)	

web3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/4766db13619a4175aa7cf834d3eeae42'))
erc20abi = json.load(open('abi/erc20.json', 'r'))


kyberrateabi = json.load(open('abi/KyberNetworkProxy.json', 'r'))
kyberratecontract = Web3.toChecksumAddress('0x9AAb3f75489902f3a48495025729a0AF77d4b11e')
kyberexchangerate = web3.eth.contract(abi=kyberrateabi, address=kyberratecontract)

#for item in dir(kyberexchangerate): print(item) # inspect properties and methods of web3 contract object

ethprovider_url = 'https://mainnet.infura.io/v3/4766db13619a4175aa7cf834d3eeae42' # infura project ID
baseaccount = Web3.toChecksumAddress('0x2e9f3eb1e287b1081f4bc8ef5adbb80f063ae19e') # pubkey

stablecoins = ["usdt", "usdc", "tusd", "dai", "busd", "husd", "pax"]

def main():
	for coin1 in stablecoins:
		for coin2 in stablecoins:
			if coin1 != coin2:
				amount = Web3.toWei(sys.argv[1], 'ETHER')
				multiplier1 =(tokenarray[coin1][1])
				multiplier2 =(tokenarray[coin2][1])
				print(tokenarray[coin1][0], tokenarray[coin2][0])
				try:
					data = getkyberprice(tokenarray[coin1][0], tokenarray[coin2][0], amount)
					print(data)
				except:pass

		



def getkyberprice(token1address, token2address, amount):
	expectedreturn = kyberexchangerate.functions.getExpectedRate(token1address, token2address, amount).call({'from': baseaccount})
	return expectedreturn

if __name__ == '__main__':
    main()