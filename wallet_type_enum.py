from enum import Enum

class WalletType(Enum):
    BTC = "BTC"
    BNB = "BNB"
    TRX = "TRX"
    BCH = "BCH"
    LTC = "LTC"
    XRP = "XRP"
    SOL = "SOL"
    DOGE = "DOGE"
    
    @staticmethod
    def get_wallet_types() -> list:
        return [wallet for wallet in WalletType]
    
    @staticmethod
    def coin_seedler(wallet_type: 'WalletType') -> str:
        from bip_utils import Bip84, Bip84Coins,  Bip44, Bip44Coins, Bip49, Bip49Coins
        wallets = {
            WalletType.BTC:(Bip84, Bip84Coins.BITCOIN),
            WalletType.BNB: (Bip44, Bip44Coins.BINANCE_SMART_CHAIN),
            WalletType.TRX:(Bip44, Bip44Coins.TRON),
            WalletType.BCH:(Bip49, Bip49Coins.BITCOIN_CASH),
            WalletType.LTC:(Bip84, Bip84Coins.LITECOIN),
            WalletType.XRP:(Bip44, Bip44Coins.RIPPLE),
            WalletType.SOL:(Bip44, Bip44Coins.SOLANA),
            WalletType.DOGE:(Bip44, Bip44Coins.DOGECOIN),
        }
        return wallets.get(wallet_type)