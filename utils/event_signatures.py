import json

FILE = "utils/event_signatures.json"

# Event signatures retrieved by the corresponding smart contract
EVENT_SIGNATURES = {
    # https://github.com/aave/aave-v3-core/blob/e46341caf815edc268893f4f9398035f242375d9/contracts/interfaces/IPool.sol#L178
    'Aave_v3_liquidations' : 'LiquidationCall(address,address,address,uint256,uint256,address,bool)',
    # https://github.com/aave/aave-protocol/blob/4b4545fb583fd4f400507b10f3c3114f45b8a037/contracts/lendingpool/LendingPool.sol#L215
    'Aave_v1_liquidations' : 'LiquidationCall(address,address,address,uint256,uint256,uint256,address,bool,uint256)',
}

if __name__=="__main__":
    with open(FILE, 'w') as jsonfile:
        json.dump(EVENT_SIGNATURES, jsonfile)