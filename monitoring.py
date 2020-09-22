import requests, logging, json, os, time, sys
from web3 import Web3

#ethereum connection and erc20 ABI import
web3 = Web3(Web3.HTTPProvider('http://192.168.1.4:3334'))

#BZRX lending contract
tokenabi = json.load(open('abi/daiLoanToken.json', 'r'))
daitokencontract = Web3.toChecksumAddress('0xdac17f958d2ee523a2206206994597c13d831ec7')
daitoken = web3.eth.contract(abi=tokenabi, address=daitokencontract)



while True:
	time.sleep(5)
	event_filter = daitoken.events.Transfer.createFilter(fromBlock="latest") 
	print(event_filter.get_all_entries())
	
	
