# Optimize XAU/USD Trading Strategy

## Overview
The `optimize_xauusd.py` script evaluates and optimizes trading strategies for XAU/USD historical data. It systematically tests various configurations of stop loss, take profit, and condition thresholds to maximize profitability while accounting for trade commissions.

## Features
- Supports a grid search across multiple parameter combinations.
- Simulates trading outcomes using realistic price movements.
- Includes configurable stop loss and take profit levels for both buy and sell trades.
- Outputs optimal parameters and associated profit.

## Outputs
1. **Optimization Results File**: `optimization_results.txt`
   - Contains the best-performing parameters.
   - Displays the maximum profit after considering trade commissions.

## Input
- A CSV file (`XAUUSD.csv`) with the following required columns:
  - `Date`: Date of the entry.
  - `Open`: Opening price.
  - `High`: Highest price.
  - `Low`: Lowest price.
  - `Close`: Closing price.

## Usage
### Prerequisites
Ensure the following Python libraries are installed:
- `pandas`
- `numpy`
- `scikit-learn`

Install dependencies using pip if necessary:
```bash
pip install pandas numpy scikit-learn
```

### Running the Script
1. Place the input CSV file (`XAUUSD.csv`) in the same directory as the script.
2. Run the script using Python:
```bash
python optimize_xauusd.py
```
3. The script will output the optimal parameters and profit to `optimization_results.txt`.

### Customization
The following parameters can be adjusted:
- `commission_per_trade`: The commission deducted per trade (default: `7`).
- `parameters`: The range and granularity of `value_a`, `sl_buy`, `tp_buy`, `sl_sell`, `tp_sell`.

Example of modifying the parameter grid:
```python
parameters = {
    "value_a": np.linspace(1, 10, 10),
    "sl_buy": np.linspace(0.5, 5, 10),
    "tp_buy": np.linspace(0.5, 10, 10),
    "sl_sell": np.linspace(0.5, 5, 10),
    "tp_sell": np.linspace(0.5, 10, 10)
}
```

### Explanation of Parameters
- **value_a**: The minimum difference between the maximum and minimum prices in the past three candles required to consider a trade.
- **sl_buy**, **tp_buy**: Stop loss and take profit levels for buy trades.
- **sl_sell**, **tp_sell**: Stop loss and take profit levels for sell trades.

## Strategy Details
### Trade Conditions
1. The script examines the last three candles to calculate:
   - **Max High**: The maximum of the `High` values.
   - **Min Low**: The minimum of the `Low` values.
2. If `Max High - Min Low` exceeds `value_a`, the script considers a trade:
   - **Buy Trade**: If the last candle's high is greater than the previous two.
   - **Sell Trade**: If the last candle's low is lower than the previous two.

### Profit Calculation
For each trade:
- **Buy Trade**:
  - Stop loss hit: `-sl_buy`
  - Take profit hit: `+tp_buy`
  - Neither hit: Profit based on the final close price.
- **Sell Trade**:
  - Stop loss hit: `-sl_sell`
  - Take profit hit: `+tp_sell`
  - Neither hit: Profit based on the final close price.

### Commission Adjustment
The total profit is reduced by the commission (`commission_per_trade`) multiplied by the total number of trades.

## Output Details
### Example Output in `optimization_results.txt`
```plaintext
Best Parameters:
value_a: 5.0
sl_buy: 2.5
tp_buy: 6.5
sl_sell: 2.0
tp_sell: 5.5

Max Profit After Commission: 1200.50
```

## Limitations
- The script assumes XAU/USD data and may require adjustments for other datasets.
- Performance depends on the quality and resolution of the input data.

## Future Enhancements
- Include additional trade parameters such as trailing stop loss.
- Visualize optimization results for better insights.
- Implement multi-threading for faster grid search.

## Author
This script is part of the **Forex XAU/USD Analysis** project by ShahramPhotonics.

