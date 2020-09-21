import requests, logging, json, os, time, sys
from web3 import Web3

web3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/4766db13619a4175aa7cf834d3eeae42'))
erc20abi = json.load(open('abi/erc20.json', 'r'))
ethprovider_url = 'https://mainnet.infura.io/v3/4766db13619a4175aa7cf834d3eeae42' # infura project ID
baseaccount = Web3.toChecksumAddress('0x2e9f3eb1e287b1081f4bc8ef5adbb80f063ae19e') # pubkey
tokens = json.load(open('abi/kyber_currencies.json', 'r'))["data"]
tokenarray = {}
for i in tokens: tokenarray[Web3.toChecksumAddress(i["address"].lower())] = (i["symbol"], 10**i["decimals"])

bzxlendingabi = json.load(open('abi/bZxProtocolLoanMaintenance.json', 'r'))
bzxlendingcontract = Web3.toChecksumAddress('0xd8ee69652e4e4838f2531732a46d1f7f584f0b7f')
bzxlending = web3.eth.contract(abi=bzxlendingabi, address=bzxlendingcontract)

ibzxabi = json.load(open('abi/IBZx.json', 'r'))
ibzx = web3.eth.contract(abi=ibzxabi, address=bzxlendingcontract)

#for item in dir(bzxlending.functions):  print(item) # inspect properties and methods of web3 contract object

unsafeloans = bzxlending.functions.getActiveLoans(0,1000000000, True).call({'from': baseaccount})

idarray = []
for loan in unsafeloans:
	idarray.append(loan[0])
	loanData = bzxlending.functions.getLoan(loan[0].hex()).call({'from': baseaccount})
	loanId = loanData[0].hex()
	endTimestamp = loanData[1]
	loanToken = loanData[2]
	collateralToken = loanData[3]
	principalhex  = loanData[4]/tokenarray[loanToken][1]
	collateral = loanData[5]
	interestOwedPerDay = loanData[6]
	interestDepositRemaining = loanData[7]
	startRate = loanData[8]
	startMargin = loanData[9]
	maintenanceMargin = loanData[10]
	currentMargin = loanData[11]
	maxLoanTerm = loanData[12]
	maxLiquidatable = loanData[13]
	maxSeizable = loanData[14]
	print("loan ID:",loanId)
	print("loan token:",tokenarray[loanToken][0])
	print("collateral token:",tokenarray[collateralToken][0])
	print("principal amount:", str(principalhex))
	#break
	
