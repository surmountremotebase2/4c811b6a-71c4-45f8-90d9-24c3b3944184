from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import ATR  # Average True Range for volatility
from surmount.logging import log

class TradingStrategy(Strategy):

    def __init__(self):
        self.tickers = ["SPY"]  # SPY as a proxy for market
        self.data_list = []

    @property
    def interval(self):
        return "1day"

    @property
    def assets(self):
        return self.tickers

    @property
    def data(self):
        return self.data_list

    def run(self, data):
        """Implements a strategy that trades on volatility.
        The strategy increases allocation to assets during periods of high volatility
        and decreases it during low volatility, as a conceptual stand-in for trading naked options."""
        
        # This example will use Average True Range as a measure of volatility
        atr = ATR("SPY", data["ohlcv"], 14)  # 14-day ATR for SPY
        
        allocation = 0.0  # Default to no allocation

        if len(atr) > 0:
            current_atr = atr[-1]
            avg_atr = sum(atr) / len(atr)

            if current_atr > avg_atr:
                log("High Volatility Detected, considering high allocation")
                allocation = 0.9  # Simulating a 'buy option' stance in high volatility
            else:
                log("Low Volatility Detected, reducing allocation")
                allocation = 0.1  # Simulating a 'sell option' stance in low volatility
        
        # Adjusted to use TargetAllocation for asset allocation
        return TargetAllocation({"SPY": allocation})