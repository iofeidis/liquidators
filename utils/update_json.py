import json

EVENT_FILE = "utils/event_signatures.json"
ASSET_FILE = "utils/asset_addresses.json"

"""
Asset Addresses retrieved manually via etherscan.io
"""
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
    '0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee': 'ETH',
    '0x80fb784b7ed66730e8b1dbd9820afd29931aab03': 'LEND',
    '0x97dec872013f6b5fb443861090ad931542878126': 'USDC',
    '0x2a1530c4c41db0b0b2bb646cb5eb1a67b7158667': 'DAI',
    '0x1985365e9f78359a9b6ad760e32412f4a445e862': 'REP',
    '0x4e3fbd56cd56c3e72c1403e103b45db9da5b9d2b': 'CVX',
    '0x111111111117dc0aa78b770fa6a738034120c302': '1INCH',
    '0x27403B2756E9c2f436FB13e0B188Dd231F1da170': 'ccrvFRAX',
    '0x27403b2756e9c2f436fb13e0b188dd231f1da170': 'ccrvFRAX',
    '0x29127fe04ffa4c32acac0ffe17280abd74eac313': 'SIFU',
    '0xd5147bc8e386d91cc5dbe72099dac6c9b99276f5': 'renFIL',
    '0x89d24a6b4ccb1b6faa2625fe562bdd9a23260359': 'SHIB',
    '0x4ddc2d193948926d02f9b1fe9e1daa0718270ed5': 'cETH',
    '0x59bd6774c22486d9f4fab2d448dce4f892a9ae25': 'f6-sOHM',
    '0x5d3a536e4d6dbd6114cc1ead35777bab948e3643': 'cDAI',
    '0x35a18000230da775cac24873d00ff85bccded550': 'cUNI',
    '0xb3319f5d18bc0d84dd1b4825dcde5d5f7266d407': 'cZRX',
    '0xe89a6d0509faf730bd707bf868d9a2a744a363c7': 'crUNI',
    '0xcbae0a83f4f9926997c8339545fb8ee32edc6b76': 'crYFI',
    '0x17107f40d70f4470d20cb3f138a052cae8ebd4be': 'crRENBTC',
    '0x892b14321a4fcba80669ae30bd0cd99a7ecf6ac0': 'crCREAM',
    '0x44fbebd2f576670a6c33f6fc0b00aa8c5753b322': 'crUSDC',
    '0x797aab1ce7c01eb727ab980762ba88e7133d2157': 'crUSDT',
    '0xc11b1268c1a384e55c48c2391d8d480264a3a7f4': 'CWBTC',
    '0x22b243b96495c547598d9042b6f94b01c22b2e9e': 'crSWAG',
    '0x158079ee67fce2f58472a96584a73c7ab9ac95c1': 'CREP',
    '0x697256caa3ccafd62bb6d3aa1c7c5671786a5fd9': 'crLINK',
    '0xeff039c3c1d668f408d09dd7b63008622a77532c': 'crWNXM',
    '0xf5dce57282a584d2746faf1593d3121fcac444dc': 'CSAI',
    '0xf650c3d88d12db855b8bf7d11be6c55a4e07dcc9': 'CUSDT',
    '0x5b37feb8fa745427892223276292889f8181b170': 'SSEAL',
    '0xdddaf1a95e57f7a74d85f366936f8a2abbc86b45': 'slELF',
    '0xce4fe9b4b8ff61949dcfeb7e03bc9faca59d2eb3': 'crBAL',
    '0x2a537fa9ffaea8c1a41d3c2b68a9cb791529366d': 'crDPI',
    '0x054b7ed3f45714d3091e82aad64a1588dc4096ed': 'crHBTC',
    '0x92b767185fb3b04f881e3ac8e5b0662a027a1d9f': 'crDAI',
    '0x8fc8bfd80d6a9f17fb98a373023d72531792b431': 'cyWBTC',
    '0x8ce5aa7812fdd6799d4c2b284a6e9f9b186e3af3': 'slSASHIMI',
    '0x24b6f00a2b5652cb81ea5b9fb5358cd759107145': 'pPIE',
    '0x8b950f43fcac4931d408f1fcda55c6cb6cbf3096': 'crBBADGER',
    '0x1d0986fb43985c88ffa9ad959cc24e6a087c7e35': 'crALPHA',
    '0x4e3a36a633f63aee0ab57b5054ec78867cb3c0b8': 'cySUSD',
    '0x697b4acaa24430f254224eb794d2a85ba1fa1fb8': 'anETH',
    '0xeebc9d3a8d93fb0516398a223aeffc0872e32cfd': 'fr4INV',
    '0x59089279987dd76fc65bf94cb40e186b96e03cb3': 'crOGN',
    '0xe2451ae4579aedaa933148481732498533db185e': 'fr7SOCKS',
    '0x4c1fdd98a179cb4ade13e8f3c063b239c9d4335f': 'zETH',
    '0x6eda4b59bac787933a4a21b65672539cef6ec97b': 'fsOHM-18',
    '0xb12b261f1c86d7f535dfea9622176bf0197e2bd0': 'pUSDC',
    '0x25942b9496282ce18c3b8d8c722ccf8e5112b252': 'zenENJ',
    '0x3774e825d567125988fb293e926064b6faa71dab': 'sUSDC',
    '0x2c4206a2bd18d581b62e793b97e89e0977619f95': 'fxICHI',
    '0xadb93a041245516a5c4538ef2bd97404cafc826c': 'G-LendWBTC',
    '0xf6551c22276b9bf62fad09f6bd6cad0264b89789': 'f6-ETH',
    '0xdbdf2fc3af896e18f2a9dc58883d12484202b57e': 'cozyUSDC',
    '0xd878726082ab9d06e863157058fb3bee50d1c41a': 'bETH',
    '0xd8553552f8868c1ef160eedf031cf0bcf9686945': 'fFEI-8',
    '0x7e9ce3caa9910cc048590801e64174957ed41d43': 'fDAI-8',
    '0xb61946a7ea4ea0b2cc605b26afef66594e77a6df': 'fXSUSHI-7',
    '0x63b63b5f0ae8057cb8f704f65fd91c19badd5a73': 'kUSDT',
    '0x45f9be645c19f07c5643599435a7b106e5d8a79c': 'dCBK',
    '0x1dca9c08e493a6a2a5ef2e3cbed0df2380245511': 'dMANA',
    '0x989273ec41274c4227bcb878c2c26fdd3afbe70d': 'fDAI-6',
    '0xca56af76b656212d768842246bf4893b56c02abc': 'f6-LINK',
    '0x63475ab76e578ec27ae2494d29e1df288817d931': 'fVVSP-23',
    '0x3fed9c8b527fa6299b3044e5178acc34ec2e25e2': 'dUSDC',
    '0xbbdc8d915bf30d53df420ecb5dc2d8fb4538ed8a': 'dAXS',
    '0x1c07bca0cee9ff1b93057d8af98f18d1c1e203c5': 'dCHZ',
    '0x4ef9faeaf702e4dce8d38cc6d2c08e66987a8106': 'fRBN-34',
    '0x17786f3813e6ba35343211bd8fe18ec4de14f28b': 'anWBTC',
    '0x4b228d99b9e5bed831b8d7d2bcc88882279a16bb': 'anINVDOLA-SLP',
    '0x86b9aa0e29cc9b1524e89c503119701f9c3bcda2': 'fPEBBLE-104',
    '0x363838fa35711ea3f8c8f95151203723cc6ee535': 'foneWING',
    '0xb2ec0d90561044aa8f09844daf417c59be5345d1': 'dSAND',
    '0x9dc533e6c168e153f0241e36e31436387631b1da': 'dPLA',
    '0x9b9b93aa9a8b3368f94b1fe87ce56034c9cba693': 'fr4LINK',
    '0xf24a7d2077285e192aa7df957a4a699c144510d8': 'sAPE',
    '0x7489c6baaba57d9a431642b26e034acd191039f7': 'D1-USDC',
    '0x3a0135418db6f9428fe669ee1162a1450612c33c': 'fFODL-127',
    '0x28af5f61544916d33c4105eb536c9177f5523b67': 'dENJ',
    '0x983e0df5cccef64fcaa54f99b0945bccf154ee80': 'qrETH',
    '0xd72929e284e8bc2f7458a6302be961b91bccb339': 'D1-ETH',
    '0x54c312ba0b974d56e2c532ca407ffda2c6a14793': 'dMATIC',
    '0x10362af7718468263243ef2419d3096a5f35c8d7': 'fUMA-128',
    '0x46fc5a5b0a68d377a75ff304556bfeea0667d3e3': 'fETH-24',
    '0xd9fe46e9a03edb7f863b5992d91ba9b24f31dded': 'fFARM-24',
    '0x26f6f27fdbc3b9cde4b1943b1c07606caf2c4c6c': 'fbveCVX-22',
    '0xcab90816f91cc25b04251857ed6002891eb0d6fa': 'apeAPE',
    '0x03c2d837e625e0f5cc8f50084b7986863c82102c': 'fcrv3crypto-156',
    '0xc6d8f83364c310304a85d7888601481e13bab440': 'fxPUNK-31',
    '0xc10d8be5c570856bec7d936d4e1e1f51308ff6d4': 'fAAVE-7',
    '0x1f947ed7ccf11d3b39fc39926c95d9d928b90e98': 'fUNI-7',
    '0xe71b4cb8a99839042c45cc4caca31c85c994e79f': 'fsteCRV-156',
    '0x8d7c80b08b8e043accc5fe24911ddc21b2408922': 'fFOXy-79',
    '0x7259ee19d6b5e755e7c65cecfd2466c09e251185': 'fwstETH-8',
    '0x53e505d422857d8f12489f7a7f0241dedd3c1ecb': 'dSHIB',
    '0x8e103eb7a0d01ab2b2d29c91934a9ad17eb54b86': 'anETHv2',
    '0xfa893f25dab476c929bf50bd43b6e2a0d53c12c7': 'fsteth-146',
    '0xe640e9bec342b86266b2bd79f3847e7958cb30c4': 'fFEI-7',
    '0xc69c916ce44f2cfa50a28e0e3002e818804217b5': 'fBNT-127',
    '0xbfd291da8a403daaf7e5e9dc1ec0aceacd4848b9': 'iwstETH',
    '0xd93f4cf882d7d576a8dc09e606b38caf18eda796': 'fETH',
    '0x109d97019eda5e32b31cd995ba3d29fc5a3e7c97': 'D1-OTHR-fl-v2',
    '0x397a7e7710f3a074da1b6823e94047e57a5db896': 'D1-MAYC-fl-v2',
    '0x5188510a48e8f716e80338c2a2ad4fc415afc290': 'D1-LAND-fl-v2',
    '0xc3d8e1fd31e55ede71ae1453ddf858461e23b59a': 'D1-BAYC-fl-v2',
    '0xccf4429db6322d5c611ee964527d42e5d685dd6a': 'cWBTC',
    '0xe4cc5a22b39ffb0a56d67f94f9300db20d786a5f': 'uneRSDL',
    '0x41c84c0e2ee0b740cf0d31f63f3b6f627dc6b393': 'cyWETH',
    '0x11c70caa910647d820bd014d676dcd97edd64a99': 'zenOM',
    '0x1637e4e9941d55703a7a5e7807d6ada3f7dcd61b': 'XINV',
    '0xa9df6bdc438a06c7946f99b6840bf412cffa3ab4': 'fRGT-7',
    '0x8b950f43fcac4931d408f1fcda55c6cb6cbf3096': 'crBBADGER',
    '0xface851a4921ce59e912d19329929ce6da6eb0c7': 'CLINK',
    '0x44fbebd2f576670a6c33f6fc0b00aa8c5753b322': 'crUSDC',
    '0xfd3300a9a74b3250f1b2abc12b47611171910b07': 'fTRIBE-8',
    '0x65b35d6eb7006e0e607bc54eb2dfd459923476fe': 'XINV',
    '0x78dcc36dc532b0def7b53a56a91610c44dd09444': 'fICHI_Vault_LP-136',
    '0x255f6afc7771c05f1a958360c414ba26d93e9a8b': 'fBPT-27',
    '0x4164e5b047842ad7dff18fc6a6e63a1e40610f46': 'sSTRK',
    '0x797aab1ce7c01eb727ab980762ba88e7133d2157': 'crUSDT',
    '0x558a7a68c574d83f327e7008c63a86613ea48b4f': 'fRGT-6',
    '0x473ccdec83b7125a4f52aa6f8699026fcb878ee8': 'kXKINE',
    '0x0bc08f2433965ea88d977d7bfded0917f3a0f60b': 'anFLOKI',
    '0xbee9cf658702527b0acb2719c1faa29edc006a92': 'sETH',
    '0xaff95ac1b0a78bd8e4f1a2933e373c66cc89c0ce': 'ICHI',
    '0x70e36f6bf80a52b3b46b3af8e106cc0ed743e8e4': 'cCOMP',
    '0x39aa39c021dfbae8fac545936693ac917d5e7563': 'cUSDC',
    '0x6c8c6b02e7b2be14d4fa6022dfd6d75921d90e4e': 'cBAT',
    '0xd06527d5e56a3495252a528c4987003b712860ee': 'crETH',
    '0x252d447c54f33e033ad04048baeade7628cb1274': 'fsOHM-36',
    '0x1066AB47a342152C564AF62D179aA4B659a11F7d': 'fSDT-27',
}

"""
Event signatures retrieved by the corresponding smart contract
Please name the events with the format : <protocol>_<version>_<event>
"""
EVENT_SIGNATURES = {
    ## AAVE
    # https://github.com/aave/aave-v3-core/blob/e46341caf815edc268893f4f9398035f242375d9/contracts/interfaces/IPool.sol#L178
    'Aave_v3_liquidations' : 'LiquidationCall(address,address,address,uint256,uint256,address,bool)',
    # https://github.com/aave/aave-protocol/blob/4b4545fb583fd4f400507b10f3c3114f45b8a037/contracts/lendingpool/LendingPool.sol#L215
    'Aave_v1_liquidations' : 'LiquidationCall(address,address,address,uint256,uint256,uint256,address,bool,uint256)',
    # https://github.com/aave/protocol-v2/blob/baeb455fad42d3160d571bd8d3a795948b72dd85/contracts/interfaces/ILendingPool.sol#L107
    'Aave_v2_flashloans' : 'FlashLoan(address,address,address,uint256,uint256,uint16)',
    # https://github.com/aave/aave-protocol/blob/4b4545fb583fd4f400507b10f3c3114f45b8a037/contracts/lendingpool/LendingPool.sol#L38
    'Aave_v1_deposits' : 'Deposit(address,address,uint256,uint16,uint256)',
    # https://github.com/aave/protocol-v2/blob/0829f97c5463f22087cecbcb26e8ebe558592c16/contracts/interfaces/ILendingPool.sol#L9
    'Aave_v2_deposits' : 'Deposit(address,address,address,uint256,uint16)',
    # https://github.com/aave/aave-protocol/blob/4b4545fb583fd4f400507b10f3c3114f45b8a037/contracts/lendingpool/LendingPool.sol#L92
    'Aave_v1_repay' : 'Repay(address,address,address,uint256,uint256,uint256,uint256)',
    # https://github.com/aave/protocol-v2/blob/0829f97c5463f22087cecbcb26e8ebe558592c16/contracts/interfaces/ILendingPool.sol#L55
    'Aave_v2_repay' : 'Repay(address,address,address,uint256)',
    # https://github.com/aave/aave-v3-core/blob/e46341caf815edc268893f4f9398035f242375d9/contracts/interfaces/IPool.sol#L74
    'Aave_v3_borrows': 'Borrow(address,address,address,uint256,uint256,uint256,uint16)',
    # https://github.com/aave/aave-v3-core/blob/e46341caf815edc268893f4f9398035f242375d9/contracts/interfaces/IPool.sol#L61
    'Aave_v3_withdraws': 'Withdraw(address,address,address,uint256)',
    
    
    ## MAKER
    # https://docs.makerdao.com/miscellaneous/liquidations-1.2-system-deprecated/cat-detailed-documentation
    'Maker_v1_Bite': 'Bite(bytes32,address,uint256,uint256,uint256,address,uint256)',
    # https://github.com/makerdao/dss/blob/17187f7d47be2f4c71d218785e1155474bbafe8a/src/dog.sol#L89
    'Maker_v2_Bark': 'Bark(bytes32,address,uint256,uint256,uint256,address,uint256)',
    
    
    ## COMPOUND
    # https://github.com/compound-finance/compound-money-market/blob/241541a62d0611118fb4e7eb324ac0f84bb58c48/contracts/MoneyMarket.sol#L169
    'Compound_v1_liquidations': 'BorrowLiquidated(address,address,uint256,uint256,uint256,uint256,address,address,uint256,uint256,uint256,uint256)',
    # https://github.com/compound-finance/compound-protocol/blob/a3214f67b73310d547e00fc578e8355911c9d376/contracts/CTokenInterfaces.sol#L149
    'Compound_v2_liquidations': 'LiquidateBorrow(address,address,uint256,address,uint256)',
    # https://github.com/compound-finance/compound-money-market/blob/241541a62d0611118fb4e7eb324ac0f84bb58c48/contracts/MoneyMarket.sol#L163
    'Compound_v1_repay': 'BorrowRepaid(address,address,uint256,uint256,uint256)',
    # https://github.com/compound-finance/compound-protocol/blob/a3214f67b73310d547e00fc578e8355911c9d376/contracts/CTokenInterfaces.sol#L143
    'Compound_v2_repay': 'RepayBorrow(address,address,uint256,uint256,uint256)',
    
    # https://github.com/compound-finance/compound-money-market/blob/241541a62d0611118fb4e7eb324ac0f84bb58c48/contracts/MoneyMarket.sol#L149
    'Compound_v1_deposits': 'SupplyReceived(address,address,uint256,uint256,uint256)',
    'Compound_v1_withdraws': 'SupplyWithdrawn(address,address,uint256,uint256,uint256)',
    'Compound_v1_borrows': 'BorrowTaken(address,address,uint256,uint256,uint256,uint256)',
    # https://github.com/compound-finance/compound-protocol/blob/a3214f67b73310d547e00fc578e8355911c9d376/contracts/CTokenInterfaces.sol#L141
    'Compound_v2_deposits': 'ReservesAdded(address,uint256,uint256)',
    'Compound_v2_withdraws': 'ReservesReduced(address,uint256,uint256)',
    'Compound_v2_borrows': 'Borrow(address,uint256,uint256,uint256)',
    # https://github.com/compound-finance/comet/blob/main/contracts/CometMainInterface.sol
    'Compound_v3_deposits': 'Supply(address,address,uint256)',

    
    
    ## LIQUITY
    # https://github.com/liquity/beta/blob/8252f7b460f2c1fb987f1dfbe9ab60c6dd1aaaac/contracts/TroveManager.sol#L192 
    'Liquity_liquidations': 'TroveLiquidated(address,uint256,uint256,uint8)',
}

if __name__=="__main__":
    """
    Run this script to update the .json files if you
    edited the values above
    """
    with open(ASSET_FILE, 'w') as jsonfile:
        json.dump(ASSET_ADDRESSES, jsonfile)
    with open(EVENT_FILE, 'w') as jsonfile:
        json.dump(EVENT_SIGNATURES, jsonfile)
