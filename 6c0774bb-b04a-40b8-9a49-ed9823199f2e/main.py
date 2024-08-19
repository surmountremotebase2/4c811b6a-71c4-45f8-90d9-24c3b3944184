from surmount.base_class import Strategy, TargetAllocation
from surmount.data import InsiderTrading, InstitutionalOwnership

class TradingStrategy(Strategy):
    def __init__(self):
        # Assuming ticker symbols for illustrative purposes. In reality, filtering for
        # specific sectors or technologies might require additional data sources or
        # a predefined list of companies involved in rocket technologies.
        self.rocket_tech_tickers = ["SPCE", "ROKT", "ASTR"]  # Fictional or placeholder tickers
        self.data_list = [InsiderTrading(ticker) for ticker in self.rocket_tech_tickers]
        self.data_list += [InstitutionalOwnership(ticker) for ticker in self.rocket_tech_tickers]

    @property
    def interval(self):
        # Daily analysis to adjust the allocation based on recent changes in insider trading
        # and institutional ownership data. This interval can be adjusted based on strategy requirements.
        return "1day"

    @property
    def assets(self):
        # Assets under consideration for this strategy
        return self.rocket_tech_tickers

    @property
    def data(self):
        # Data required for decision making in the strategy
        return self.data_list

    def run(self, data):
        allocations = {}
        for ticker in self.rocket_tech_tickers:
            insider_data_key = ("insider_trading", ticker)
            institution_data_key = ("institutional_ownership", ticker)

            insider_data = data.get(insider_data_key, [])
            institution_data = data.get(institution_data_key, [])

            # Placeholder logic to "score" companies based on insider buying activity and institutional ownership
            insider_buying = any(i['transactionType'] in ["Purchase", "Buy"] for i in insider_data)

            # Check if there is significant institutional ownership, this part is arbitrary and
            # in a real strategy might involve specific thresholds or comparisons
            has_significant_institutional_ownership = any(i['ownershipPercent'] >= 50 for i in institution_data)

            # If both positive insider buying and substantial institutional ownership are observed,
            # the company is considered a strong candidate
            if insider_buying and has_significant_institutional_ownership:
                allocations[ticker] = 1 / len(self.rocket_tech_tickers)
            else:
                allocations[ticker] = 0

        return TargetAllocation(allocations)