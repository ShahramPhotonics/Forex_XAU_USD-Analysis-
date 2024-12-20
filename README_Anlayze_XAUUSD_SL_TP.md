# Forex XAUUSD Analysis and Optimization

## Overview

This repository contains Python scripts and data files for analyzing and optimizing trading strategies for XAU/USD based on historical candle data. The scripts generate CSV files with calculated metrics, price breakdowns, and optimized strategies to help users determine the best stop-loss and take-profit levels.

---

## Files and Scripts

### 1. **Python Scripts**
- **`Analyze_XAUUSD_SL_TP.py`**: 
  - Generates the following datasets:
    - **Sheet1_Gap_4_Candles.csv**: Calculates the difference (Gap) between the highest high and lowest low of the first 4 candles.
    - **Sheet2_Opening_5th_Candle.csv**: Records the opening price of the 5th candle after the 4-candle gap.
    - **Sheet3_Max_Min_Next_4.csv**: Determines the maximum and minimum prices from the next 4 candles after the 5th candle.
    - **Sheet4_Bid_Ask_Prices.csv**: Generates bid and ask prices for each candle (open, low, high, and close) with an added spread of 0.7.
    - **Sheet5_Increased_Resolution_Prices.csv**: Increases price resolution by interpolating between open, low, high, and close prices in steps, rounded to two decimal places.
  - Filters and processes data to analyze conditions for stop-loss and take-profit.

- **`Optimize_XAUUSD.py`** *(future integration)*:
  - Neural network optimization to find the best stop-loss and take-profit levels based on historical data.

---

### 2. **CSV Outputs**
- **`Sheet1_Gap_4_Candles.csv`**: Contains gap values for the first 4 candles.
- **`Sheet2_Opening_5th_Candle.csv`**: Contains the opening price of the 5th candle.
- **`Sheet3_Max_Min_Next_4.csv`**: Records max and min values from the next 4 candles.
- **`Sheet4_Bid_Ask_Prices.csv`**: Includes bid and ask prices for each candle's price points (open, low, high, close).
- **`Sheet5_Increased_Resolution_Prices.csv`**: Expanded price data with finer resolution.

---

## Requirements

- Python 3.10 or compatible version
- Required libraries:
  - `pandas`
  - `numpy`
  - `openpyxl` (for Excel writing if needed)

Install required libraries:
```bash
pip install pandas numpy openpyxl
```

---

## How to Use

1. Clone the repository:
   ```bash
   git clone https://github.com/ShahramPhotonics/Forex_XAU_USD-Analysis.git
   ```
2. Navigate to the project directory:
   ```bash
   cd Forex_XAU_USD-Analysis
   ```
3. Run the analysis script:
   ```bash
   python Analyze_XAUUSD_SL_TP.py
   ```
   - CSV outputs will be saved in the same directory.

---

## Next Steps

1. **Optimization**:
   - The next step involves running `Optimize_XAUUSD.py` to determine optimal stop-loss and take-profit strategies using neural network models.

2. **Visualization**:
   - Incorporate plots for visualizing the relationships between gaps, max/min values, and profitability probabilities.

---

## Contribution
Feel free to fork this repository and contribute improvements, bug fixes, or additional analysis features!
