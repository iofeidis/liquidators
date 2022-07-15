import json

FILE = "utils/asset_addresses.json"

# Asset Addresses retrieved manually via etherscan.io
ASSET_ADDRESSES = {
    '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2': 'WETH',
    '0x514910771af9ca656af840dff83e8264ecf986ca': 'LINK',
    '0x2260fac5e5542a773aa44fbcfedf7c193bc2c599': 'WBTC',
    '0x7fc66500c84a76ad7e9c93437bfc5ac33e2ddae9': 'AAVE',
    '0x1f9840a85d5af5bf1d1762f925bdaddc4201f984': 'UNI',
    '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48': 'USDC',
    '0x0f5d2fb29fb7d3cfee444a200298f468908cc942': 'MANA',
    '0xae7ab96520de3a18e5e111b5eaab095312d7fe84': 'stETH',
    '0xf629cbd94d3791c9250152bd8dfbdf380e2a3b9c': 'ENJ',
    '0x408e41876cccdc0f92210600ef50372656052a38': 'REN',
    '0xd533a949740bb3306d119cc777fa900ba034cd52': 'CRV',
    '0x8798249c2e607446efb7ad49ec89dd1865ff4272': 'xSUSHI',
    '0x0bc529c00c6401aef6d220be8c6ea1667f6ad93e': 'YFI',
    '0x9f8f72aa9304c8b593d555f12ef6589cc3a579a2': 'MKR',
    '0x6b175474e89094c44da98b954eedeac495271d0f': 'DAI',
    '0x0d8775f648430679a709e98d2b0cb6250d2887ef': 'BAT',
    '0xc011a73ee8576fb46f5e1c5751ca3b9fe0af2a6f': 'SNX',
    '0xe41d2489571d322189246dafa5ebde1f4699f498': 'ZRX',
    '0xdd974d5c2e2928dea5f71b9825b8b646686bd200': 'KNC',
    '0xba100000625a3754423978a60c9317c58a424e3d': 'BAL',
    '0x1494ca1f11d487c2bbe4543e90080aeba4ba3c2b': 'DPI',
    '0x59a19d8c652fa0284f44113d0ff9aba70bd46fb4': 'BPT',
    '0xc18360217d8f7ab5e7c516566761ea12ce7f9d72': 'ENS',
    '0x0000000000085d4780b73119b644ae5ecd22b376': 'TUSD',
    '0xbb2b8038a1640196fbe3e38816f3e67cba72d940': 'UNI-V2:WBTC',
    '0xa2107fa5b38d9bbd2c461d6edf11b11a50f6b974': 'UNI-V2',
    '0xdfc14d2af169b0d36c4eff567ada9b2e0cae044f': 'UNI-V2',
    '0xd3d2e2692501a5c9ca623199d38826e513033a17': 'UNI-V2',
    '0xa478c2975ab1ea89e8196811f51a7b7ade33eb11': 'UNI-V2',
    '0x3da1313ae46132a397d90d95b1424a9a7e3e0fce': 'UNI-V2',
    '0x004375dff511095cc5a197a54140a24efef3a416': 'UNI-V2',
    '0x956f47f50a910163d8bf957cf5846d573e7f87ca': 'FEI',
    '0xdac17f958d2ee523a2206206994597c13d831ec7': 'USDT',
    '0x056fd409e1d7a124bd7017459dfea2f387b6d5cd': 'GUSD',
    '0x4fabb145d64652a948d72533023f6e7a623c7c53': 'BUSD',
    '0x57ab1ec28d129707052df4df418d58a2d46d5f51': 'sUSD',
    '0x8e870d67f660d95d5be530380d0ec0bd388289e1': 'USDP',
    '0x853d955acef822db058eb8505911ed77f175b99e': 'FRAX',
    '0x03ab458634910aad20ef5f1c8ee96f1d6ac54919': 'RAI',
    '0xd46ba6d942050d489dbd938a2c909a5d5039a161': 'AMPL',
    '0xa693b19d2931d498c5b318df961919bb4aee87a5': 'UST',
    '0x408e41876cccdc0f92210600ef50372656052a38': 'REN',   
}

if __name__=="__main__":
    with open(FILE, 'w') as jsonfile:
        json.dump(ASSET_ADDRESSES, jsonfile)