# Analyze XAU/USD Data

## Overview
The `analyze_xauusd.py` script performs in-depth analysis on XAU/USD historical data. It identifies patterns based on specified conditions and outputs the results in a detailed Excel file and a summarized text file. This tool is ideal for evaluating trends and behaviors in financial data for the XAU/USD pair.

## Features
- Processes historical data to examine conditions involving price ranges across multiple rows.
- Generates an Excel file with analysis sheets starting from different rows to ensure robustness.
- Summarizes critical ratios (I4) in a text file for easy interpretation.
- Allows customizable thresholds for analysis (`Value_A`).

## Outputs
1. **Excel File**: `result.xlsx`
   - Contains multiple sheets (one per condition and starting row) with detailed analysis.
   - Each sheet includes:
     - Calculated deltas, extreme prices, and additional computed columns.
     - Ratios of specific conditions met (I2, I3, I4).
2. **Text File**: `summary.txt`
   - Summarizes I4 ratios for each threshold, presented concisely for quick evaluation.

## Input
- A CSV file (`XAUUSD.csv`) with the following required columns:
  - `date`: Date of the entry.
  - `open`: Opening price.
  - `high`: Highest price.
  - `low`: Lowest price.
  - `close`: Closing price.

## Usage
### Prerequisites
Ensure the following Python libraries are installed:
- `pandas`
- `openpyxl`

Install dependencies using pip if necessary:
```bash
pip install pandas openpyxl
```

### Running the Script
1. Place the input CSV file (`XAUUSD.csv`) in the same directory as the script.
2. Run the script using Python:
```bash
python analyze_xauusd.py
```
3. Outputs:
   - `result.xlsx` will contain detailed analyses.
   - `summary.txt` will include summarized ratios.

### Customization
You can modify the maximum value for `Value_A` in the script by adjusting the `max_value` parameter. For example:
```python
analyze_xauusd_data('XAUUSD.csv', 'result.xlsx', 'summary.txt', max_value=50)
```
This will analyze conditions from 1 to 50.

## Details of the Analysis
### Excel File
Each sheet corresponds to one starting row (1 to 8) and includes:
- **Row Number**: Sequential identifier of the analyzed rows.
- **Delta (Max-Min)**: Difference between maximum and minimum prices for the first three rows.
- **First Open Price**: Opening price of the row following the first three rows.
- **First Extreme**: The first extreme (maximum or minimum) from the next five rows.
- **Second Extreme**: The opposite extreme from the next five rows.
- **Delta (Next 5 Rows)**: Difference between the maximum and minimum prices in the next five rows.
- **Column G (D-C)**: Difference between the first extreme and the first open price.
- **Column H (E-C)**: Difference between the second extreme and the first open price.
- **I2**: Count of positive differences greater than 1 in Column G.
- **I3**: Count of negative differences less than -1 in Column G.
- **I4**: Ratio of I2 to I3.

### Text File
The `summary.txt` file contains the summarized I4 ratios for all condition thresholds, formatted as:
```plaintext
1: [value1, value2, ..., value8]
2: [value1, value2, ..., value8]
...
30: [value1, value2, ..., value8]
```
Each line corresponds to a condition value, listing the ratios for all 8 starting rows.

## Limitations
- Ensure the input CSV file has no missing or invalid data.
- Designed specifically for XAU/USD data; may require adjustments for other datasets.

## Future Enhancements
- Automate the detection of anomalies in price movements.
- Include visualization of results directly in the Excel file.

## Author
This script is part of the **Forex XAU/USD Analysis** project by ShahramPhotonics.

