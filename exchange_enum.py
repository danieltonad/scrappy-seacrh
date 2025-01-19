from enum import Enum

class Exchange(Enum):
    BINANCE = "BINANCE"
    BYBIT = "BYBIT"
    MEXC = "MEXC"
    
    
    @staticmethod
    def get_exchanges() -> list:
        return [exchange for exchange in Exchange]
    
    @staticmethod
    def get_exchange_uid(exchange: 'Exchange') -> str:
        from settings import settings
        exchanges = {
            Exchange.BINANCE: settings.BINANCE_UID,
            Exchange.BYBIT: settings.BYBIT_UID,
            Exchange.MEXC: settings.MEXC_UID,
        }
        return exchanges.get(exchange)
        