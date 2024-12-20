import pandas as pd
import numpy as np
from sklearn.model_selection import ParameterGrid

# Load CSV file
data = pd.read_csv("XAUUSD.csv", parse_dates=["Date"], index_col="Date")

# Function to calculate profit/loss
def calculate_profit_loss(open_price, high, low, sl, tp, position):
    if position == "buy":
        # Sequence: Open -> Low -> High -> Close
        if low <= open_price - sl:  # Stop loss hit
            return -sl
        elif high >= open_price + tp:  # Take profit hit
            return tp
        else:  # Neither hit, close at the end of the candle
            return open_price - low
    elif position == "sell":
        # Sequence: Open -> High -> Low -> Close
        if high >= open_price + sl:  # Stop loss hit
            return -sl
        elif low <= open_price - tp:  # Take profit hit
            return tp
        else:  # Neither hit, close at the end of the candle
            return high - open_price

# Strategy function
def strategy(data, value_a, sl_buy, tp_buy, sl_sell, tp_sell):
    profits = []
    trade_count = 0
    for i in range(3, len(data)):
        highs = data['High'].iloc[i-3:i].values
        lows = data['Low'].iloc[i-3:i].values
        open_price = data['Open'].iloc[i]

        max_high = np.max(highs)
        min_low = np.min(lows)

        if max_high - min_low < value_a:
            continue

        if highs[-1] > highs[-2] and highs[-1] > highs[-3]:  # Open Buy
            profit = calculate_profit_loss(open_price, highs[-1], lows[-1], sl_buy, tp_buy, "buy")
            profits.append(profit)
            trade_count += 1

        elif lows[-1] < lows[-2] and lows[-1] < lows[-3]:  # Open Sell
            profit = calculate_profit_loss(open_price, highs[-1], lows[-1], sl_sell, tp_sell, "sell")
            profits.append(profit)
            trade_count += 1

    total_profit = np.sum(profits)
    return total_profit, trade_count

# Optimization
parameters = {
    "value_a": np.linspace(1, 10, 10),
    "sl_buy": np.linspace(0.5, 5, 10),
    "tp_buy": np.linspace(0.5, 10, 10),
    "sl_sell": np.linspace(0.5, 5, 10),
    "tp_sell": np.linspace(0.5, 10, 10)
}
param_grid = list(ParameterGrid(parameters))

best_profit = -np.inf
best_params = None

commission_per_trade = 7  # Example realistic commission per lot (round trip)

for params in param_grid:
    value_a = params['value_a']
    sl_buy = params['sl_buy']
    tp_buy = params['tp_buy']
    sl_sell = params['sl_sell']
    tp_sell = params['tp_sell']

    profit, trade_count = strategy(data, value_a, sl_buy, tp_buy, sl_sell, tp_sell)
    profit_after_commission = profit - trade_count * commission_per_trade

    if profit_after_commission > best_profit:
        best_profit = profit_after_commission
        best_params = params

# Write results to a text file
with open("optimization_results.txt", "w") as f:
    f.write("Best Parameters:\n")
    for key, value in best_params.items():
        f.write(f"{key}: {value}\n")
    f.write(f"\nMax Profit After Commission: {best_profit}\n")

print("Optimization completed. Results saved to optimization_results.txt.")
