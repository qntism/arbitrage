import requests, logging, json, os, time, sys
from web3 import Web3

#ethereum connection and erc20 ABI import
web3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/4766db13619a4175aa7cf834d3eeae42'))
erc20abi = json.load(open('abi/erc20.json', 'r'))
baseaccount = Web3.toChecksumAddress('0x2e9f3eb1e287b1081f4bc8ef5adbb80f063ae19e') # pubkey

#makes array of token addresses with the symbol and decimals
tokens = json.load(open('abi/kyber_currencies.json', 'r'))["data"]
tokenarray = {}
for i in tokens: tokenarray[Web3.toChecksumAddress(i["address"].lower())] = (i["symbol"], 10**i["decimals"])

#BZRX lending contract
bzxlendingabi = json.load(open('abi/bZxProtocolLoanMaintenance.json', 'r'))
bzxlendingcontract = Web3.toChecksumAddress('0xd8ee69652e4e4838f2531732a46d1f7f584f0b7f')
bzxlending = web3.eth.contract(abi=bzxlendingabi, address=bzxlendingcontract)

#BZRX inherited
ibzxabi = json.load(open('abi/IBZx.json', 'r'))
ibzx = web3.eth.contract(abi=ibzxabi, address=bzxlendingcontract)

#AAVE Lending Pool contract
aavelendingabi = json.load(open('abi/aavelendingpool.json', 'r'))
aavelendingcontract = Web3.toChecksumAddress('0x398eC7346DcD622eDc5ae82352F02bE94C62d119')
aavelending = web3.eth.contract(abi=aavelendingabi, address=aavelendingcontract)

#inspect functions and methods of web3 contract object
#for item in dir(bzxlending.functions):  print(item) 

#creates contract object for getting unhealthy BZRX loans
unsafeloans = bzxlending.functions.getActiveLoans(0,1000000000, True).call({'from': baseaccount})

#main function to loop through unhealthy loans and locate profitable liquidations
def main():
	#while True:
	for loan in unsafeloans:
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
	

#call main function
if __name__ == '__main__':
    main()
















