import pandas as pd
import numpy as np

# Generate bid and ask price sequences
def generate_tick_data(data):
    expanded_data = []
    for _, row in data.iterrows():
        open_price = row['open']
        low_price = row['low']
        high_price = row['high']
        close_price = row['close']

        # Generate bid prices: open → low → high → close
        bid_prices = np.round(np.concatenate([
            np.arange(open_price, low_price, -0.30),  # Open to Low
            np.arange(low_price, high_price, 0.30),  # Low to High
            np.arange(high_price, close_price, -0.30)  # High to Close
        ]), 2)
        bid_prices = np.append(bid_prices, close_price)

        # Generate ask prices by adding 0.70 and rounding
        ask_prices = np.round(bid_prices + 0.70, 2)

        # Append expanded prices to the same row
        for bid, ask in zip(bid_prices, ask_prices):
            expanded_data.append({
                'date': row['date'],
                'original_open': row['open'],
                'original_high': row['high'],
                'original_low': row['low'],
                'original_close': row['close'],
                'bid': bid,
                'ask': ask
            })

    return pd.DataFrame(expanded_data)

# OnTick function to simulate price updates
def on_tick(data, lot_sizes, stop_loss, take_profit):
    index = 0
    total_pips = 0
    position_volume = lot_sizes[index] * 0.01
    trade_details = []
    active_trade = None

    for _, row in data.iterrows():
        bid_price = row['bid']
        ask_price = row['ask']
        candle_frame = data[data['date'] == row['date']].head(4)  # Track last 4 candles

        if active_trade:
            # Check stop loss or take profit
            if bid_price <= active_trade['stop_loss']:
                # Stop loss hit
                trade_details.append({
                    'entry_price': active_trade['entry_price'],
                    'exit_price': active_trade['stop_loss'],
                    'profit_loss_pips': (active_trade['stop_loss'] - active_trade['entry_price']) * 100 * position_volume,
                    'volume': position_volume,
                    'index': index
                })
                total_pips += (active_trade['stop_loss'] - active_trade['entry_price']) * 100 * position_volume
                index = (index + 1) % len(lot_sizes)
                position_volume = lot_sizes[index] * 0.01
                active_trade = None  # Close the trade
            elif ask_price >= active_trade['take_profit']:
                # Take profit hit
                trade_details.append({
                    'entry_price': active_trade['entry_price'],
                    'exit_price': active_trade['take_profit'],
                    'profit_loss_pips': (active_trade['take_profit'] - active_trade['entry_price']) * 100 * position_volume,
                    'volume': position_volume,
                    'index': index
                })
                total_pips += (active_trade['take_profit'] - active_trade['entry_price']) * 100 * position_volume
                index = 0
                position_volume = lot_sizes[index] * 0.01
                active_trade = None  # Close the trade
        else:
            # Check criteria for new 'buy' position
            max_high = candle_frame['original_high'].max()
            min_low = candle_frame['original_low'].min()
            if (max_high - min_low > 1.00) and (ask_price > max_high):
                entry_price = ask_price
                active_trade = {
                    'entry_price': entry_price,
                    'stop_loss': round(entry_price - stop_loss, 2),
                    'take_profit': round(entry_price + take_profit, 2)
                }

    # Write trade details to a file
    with open('trade_details.txt', 'w') as f:
        for trade in trade_details:
            f.write(f"Entry: {trade['entry_price']}, Exit: {trade['exit_price']}, "
                    f"P/L: {trade['profit_loss_pips']:.2f}, Volume: {trade['volume']:.2f}, Index: {trade['index']}\n")

    return total_pips

# Load data and generate ticks
file_path = 'XAUUSD.csv'
data = pd.read_csv(file_path)
data.columns = [col.strip().lower() for col in data.columns]
data['date'] = pd.to_datetime(data['date'])
tick_data = generate_tick_data(data)

# Backtest parameters
lot_sizes = [1, 3, 6, 10, 21]
stop_loss = 1.00
take_profit = 1.00


# Run backtest
total_pips = on_tick(tick_data, lot_sizes, stop_loss, take_profit)
print(f"Total profit from the strategy: {total_pips:.2f} pips")
