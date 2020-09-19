# using orfeed price oracle for uniswap
import requests, logging, json, os, time, sys
from web3 import Web3

class uniswapprice:
	def main(source, destination, useramount):

			tokens = json.load(open('abi/kyber_currencies.json', 'r'))["data"]
			tokenarray = {}
			for i in tokens: tokenarray[i["symbol"].lower()] = (Web3.toChecksumAddress(i["address"]), i["decimals"])
			#print(tokenarray)	

			web3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/4766db13619a4175aa7cf834d3eeae42'))
			erc20abi = json.load(open('abi/erc20.json', 'r'))
			amount = Web3.toWei(useramount, 'ETHER')

			uniswapabi= json.load(open('abi/UniswapV2Router02.json', 'r'))
			uniswapcontract = Web3.toChecksumAddress('0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D')
			uniswap = web3.eth.contract(abi=uniswapabi, address=uniswapcontract)

			#for item in dir(uniswap.functions): print(item) # inspect properties and methods of web3 contract object

			ethprovider_url = 'https://mainnet.infura.io/v3/4766db13619a4175aa7cf834d3eeae42' # infura project ID
			baseaccount = Web3.toChecksumAddress('0x2e9f3eb1e287b1081f4bc8ef5adbb80f063ae19e') # pubkey

			
			
			def getuniswapprice(token1address, token2address, amount):
				expectedreturn = uniswap.functions.getAmountsOut(amount, (token1address, token2address)).call({'from': baseaccount})[1]
				return float(expectedreturn/10**tokenarray[destination][1])


			afterslippage = getuniswapprice(tokenarray[source][0], tokenarray[destination][0], amount)
			output = str(amount) + " " + source + " after slippage will get " + str(afterslippage) + " " + destination
			return afterslippage
	


















