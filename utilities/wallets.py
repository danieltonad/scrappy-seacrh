from enum import Enum
from httpx import AsyncClient

class WalletType(Enum):
    BTC = "BTC"
    BNB = "BNB"
    TRX = "TRX"
    
    @staticmethod
    def get_wallet_types() -> list:
        return [wallet for wallet in WalletType]
    
    @staticmethod
    def get_wallet_type_name(wallet_type: 'WalletType') -> str:
        wallets = {
            WalletType.BTC:"BITCOIN",
            WalletType.BNB:"BNB (BEP20)",
            WalletType.TRX:"TRON (TRC20)",
        }
        return wallets.get(wallet_type)
    
    @staticmethod
    def coin_seedler(wallet_type: 'WalletType') -> str:
        from bip_utils import Bip84, Bip84Coins,  Bip44, Bip44Coins
        wallets = {
            WalletType.BTC:(Bip84, Bip84Coins.BITCOIN),
            WalletType.BNB: (Bip44, Bip44Coins.BINANCE_SMART_CHAIN),
            WalletType.TRX:(Bip44, Bip44Coins.TRON)
        }
        return wallets.get(wallet_type)
    
    @staticmethod
    def balance_service(wallet_type: 'WalletType'):
        from services.balance import get_btc_balance, get_bnb_balance, get_trx_balance
        wallets = {
            WalletType.BTC: get_btc_balance,
            WalletType.BNB: get_bnb_balance,
            WalletType.TRX: get_trx_balance
        }
        return wallets.get(wallet_type)
    
    @staticmethod
    async def price_service(wallet_type: 'WalletType', session: AsyncClient):
        from services.balance import get_coin_current_price
        wallets = {
            WalletType.BTC: "bitcoin",
            WalletType.BNB: "binancecoin",
            WalletType.TRX: "tron"
        }
        return await get_coin_current_price(session=session, coin=wallets.get(wallet_type))