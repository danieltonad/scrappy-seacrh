from enum import Enum

class WalletType(Enum):
    BTC = "BTC"
    BNB = "BNB"
    TRX = "TRX"
    
    @staticmethod
    def get_wallet_types() -> list:
        return [wallet for wallet in WalletType]
    
    @staticmethod
    def coin_seedler(wallet_type: 'WalletType') -> str:
        from bip_utils import Bip84, Bip84Coins,  Bip44, Bip44Coins
        wallets = {
            WalletType.BTC:(Bip84, Bip84Coins.BITCOIN),
            WalletType.BNB: (Bip44, Bip44Coins.BINANCE_SMART_CHAIN),
            WalletType.TRX:(Bip44, Bip44Coins.TRON)
        }
        return wallets.get(wallet_type)