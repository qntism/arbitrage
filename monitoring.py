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
	
#[AttributeDict({'args': AttributeDict({'from': '0x0D0707963952f2fBA59dD06f2b425ace40b492Fe', 'to': '0x5a2384acC7bB8e749d257520D5195DC72F3631D7', 'value': 1001000000}), 'event': 'Transfer', 'logIndex': 17, 'transactionIndex': 62, 'transactionHash': HexBytes('0x9cda8777faf9ee274a08e94015c23f269f2ef0bd39805b29af3bbbf9f1f6579b'), 'address': '0xdAC17F958D2ee523a2206206994597C13D831ec7', 'blockHash': HexBytes('0x1bbd4afc0d8ef2ed0022a0d8573ee43c004042df300a38248b571f4f51b37511'), 'blockNumber': 5851448})]	
	
