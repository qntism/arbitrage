import requests, logging, json, os, time, sys
from web3 import Web3

#ethereum connection and erc20 ABI import
web3 = Web3(Web3.HTTPProvider('http://192.168.1.4:3334'))

#BZRX lending contract
tokenabi = json.load(open('abi/daiLoanToken.json', 'r'))
tokencontract = Web3.toChecksumAddress('0xdac17f958d2ee523a2206206994597c13d831ec7')
token = web3.eth.contract(abi=tokenabi, address=tokencontract)

#makes array of token addresses with the symbol and decimals
tokens = json.load(open('abi/kyber_currencies.json', 'r'))["data"]
tokenarray = {}
for i in tokens: tokenarray[i["address"].lower()] = (i["symbol"].lower(), 10**i["decimals"])

#output log file
ofile = open("ethlogs.txt", "w+")


while True:
	print("searching...")
	event_filter = token.events.Transfer.createFilter(fromBlock="latest") 
	count = 0
	for item in event_filter.get_all_entries():
		count += 1
		saddress = item["args"]["from"]
		daddress = item["args"]["to"]
		amount = item["args"]["value"]/10**6
		tx = item["transactionHash"].hex()
		symbol = tokenarray["0xdac17f958d2ee523a2206206994597c13d831ec7".lower()][0]
		blocknumber = item["blockNumber"]
		output = str((symbol, saddress, daddress, amount, tx, blocknumber))
		ofile.write(output)		
		print(symbol, saddress, daddress, amount, tx, blocknumber)
	count = 0
	time.sleep(10)
	
#[AttributeDict({'args': AttributeDict({'from': '0x0D0707963952f2fBA59dD06f2b425ace40b492Fe', 'to': '0x5a2384acC7bB8e749d257520D5195DC72F3631D7', 'value': 1001000000}), 'event': 'Transfer', 'logIndex': 17, 'transactionIndex': 62, 'transactionHash': HexBytes('0x9cda8777faf9ee274a08e94015c23f269f2ef0bd39805b29af3bbbf9f1f6579b'), 'address': '0xdAC17F958D2ee523a2206206994597C13D831ec7', 'blockHash': HexBytes('0x1bbd4afc0d8ef2ed0022a0d8573ee43c004042df300a38248b571f4f51b37511'), 'blockNumber': 5851448})]	
	
