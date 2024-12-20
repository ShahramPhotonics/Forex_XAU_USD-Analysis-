import pandas as pd
import numpy as np

# Load the data file (replace 'XAUUSD.csv' with your actual file path)
data_file = 'XAUUSD.csv'
data = pd.read_csv(data_file)

# Ensure the column names match your data
data.columns = ['timestamp', 'open', 'high', 'low', 'close']

# Create Sheet1: Difference (max - min) of first 4 candles
sheet1_df = pd.DataFrame()
sheet1_df['Gap_4_Candles'] = data['high'].rolling(window=4).max() - data['low'].rolling(window=4).min()

# Create Sheet2: Opening price of 5th candle
sheet2_df = pd.DataFrame()
sheet2_df['Opening_5th_Candle'] = data['open'].shift(-4)

# Create Sheet3: Max and Min of next 4 candles after 5th
sheet3_df = pd.DataFrame()
sheet3_df['Max_Next_4'] = data['high'].shift(-4).rolling(window=4).max()
sheet3_df['Min_Next_4'] = data['low'].shift(-4).rolling(window=4).min()

# Combine Sheet1, Sheet2, and Sheet3
combined_df = pd.concat([sheet1_df, sheet2_df, sheet3_df], axis=1)

# Filter conditions
combined_df['Difference_Max_Open'] = combined_df['Max_Next_4'] - combined_df['Opening_5th_Candle']
combined_df['Difference_Min_Open'] = combined_df['Min_Next_4'] - combined_df['Opening_5th_Candle']
filtered_df = combined_df[combined_df['Difference_Max_Open'] > 0]

# Create Sheet4: Bid and Ask price generation with breakdown
sheet4_df = pd.DataFrame()
sheet4_data = []
for i, row in data.iterrows():
    candle_number = i + 1
    bid_prices = [row['open'], row['low'], row['high'], row['close']]
    ask_prices = [bid + 0.7 for bid in bid_prices]
    for bid, ask in zip(bid_prices, ask_prices):
        sheet4_data.append([candle_number, bid, ask])
sheet4_df = pd.DataFrame(sheet4_data, columns=['Candle_Number', 'Bid_Price', 'Ask_Price'])

# Create Sheet5: Increased resolution of prices
sheet5_df = pd.DataFrame()
sheet5_data = []
for i, row in data.iterrows():
    candle_number = i + 1
    prices = np.linspace(row['open'], row['low'], num=10).tolist() + \
             np.linspace(row['low'], row['high'], num=10).tolist() + \
             np.linspace(row['high'], row['close'], num=10).tolist()
    for price in prices:
        sheet5_data.append([candle_number, round(price, 2)])
sheet5_df = pd.DataFrame(sheet5_data, columns=['Candle_Number', 'Price'])

# Save all sheets to separate CSV files
sheet1_df.to_csv('Sheet1_Gap_4_Candles.csv', index=False)
sheet2_df.to_csv('Sheet2_Opening_5th_Candle.csv', index=False)
sheet3_df.to_csv('Sheet3_Max_Min_Next_4.csv', index=False)
sheet4_df.to_csv('Sheet4_Bid_Ask_Prices.csv', index=False)
sheet5_df.to_csv('Sheet5_Increased_Resolution_Prices.csv', index=False)

print("All sheets successfully written to separate CSV files.")
