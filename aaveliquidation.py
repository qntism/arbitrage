import requests, logging, json, os, time, sys
from web3 import Web3

r = requests.get('https://protocol-api.aave.com/liquidations?get=proto')
data = json.loads(r.text)

web3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/4766db13619a4175aa7cf834d3eeae42'))
erc20abi = json.load(open('abi/erc20.json', 'r'))

accounts = {}
for item in data["data"]:
	user = (item["user"]["id"])
	hf = (item["user"]["healthFactor"])
	accounts[user] = hf
	
aavelendingabi = json.load(open('abi/aavelendingpool.json', 'r'))
aavelendingcontract = Web3.toChecksumAddress('0x398eC7346DcD622eDc5ae82352F02bE94C62d119')
aavelending = web3.eth.contract(abi=aavelendingabi, address=aavelendingcontract)

#for item in dir(aavelending.functions): print(item) # inspect properties and methods of web3 contract object

ethprovider_url = 'https://mainnet.infura.io/v3/4766db13619a4175aa7cf834d3eeae42' # infura project ID
baseaccount = Web3.toChecksumAddress('0x2e9f3eb1e287b1081f4bc8ef5adbb80f063ae19e') # pubkey

for address,hf in accounts.items():
	address = Web3.toChecksumAddress(address)
	useraccountdata = aavelending.functions.getUserAccountData(address).call({'from': baseaccount})
	health = useraccountdata[7]
	if len(str(health)) == 18:
		print(address,str(int(health)/10**18))
