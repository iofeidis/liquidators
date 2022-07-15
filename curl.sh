curl -X POST -H "Content-Type: application/json" --data \
	'{"jsonrpc":"2.0","method":"eth_getLogs","params":[{
		"fromBlock": 10000000,
       		"toBlock": 11000000, 
		"topics": [
			["0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"],
			["0x0000000000000000000000008bfbb529a9e85fdc4b70a4fcdc0d68bb298b8816"]
		]
	}],
	"id":3}' http://127.0.0.1:8545
