import pandas as pd

def analyze_xauusd_data(input_file, output_file, summary_file, max_value=5):
    # Read the data from the CSV file
    data = pd.read_csv(input_file)

    # Ensure the data has the expected columns
    if not {'date', 'open', 'high', 'low', 'close'}.issubset(data.columns):
        raise ValueError("The input file must contain 'date', 'open', 'high', 'low', 'close' columns.")

    summaries = []  # To store summarized I4 values for all conditions

    with pd.ExcelWriter(output_file, mode='w') as writer:
        for value_a in range(1, max_value + 1):
            condition_ratios = []  # To store I4 values for this condition

            for sheet_num in range(8):
                start_row = sheet_num + 1
                results = []  # To store results for the current sheet

                # Examine rows in steps of 8 starting from the current start_row
                i = start_row
                while i < len(data) - 7:
                    # Extract three rows
                    segment = data.iloc[i:i+3]

                    # Calculate max and min prices for the three rows
                    max_price = segment['high'].max()
                    min_price = segment['low'].min()

                    # Calculate the delta
                    delta = max_price - min_price

                    # Check the condition
                    if delta > value_a:
                        first_open_price = data.iloc[i + 3]['open'] if i + 3 < len(data) else None

                        # Extract the next 5 rows
                        next_candles = data.iloc[i+3:i+8]

                        # Determine which extreme (max or min) occurs first
                        first_extreme = None
                        second_extreme = None

                        for index, row in next_candles.iterrows():
                            if first_extreme is None:
                                if row['high'] == next_candles['high'].max():
                                    first_extreme = row['high']
                                    second_extreme = next_candles['low'].min()
                                    break
                                elif row['low'] == next_candles['low'].min():
                                    first_extreme = row['low']
                                    second_extreme = next_candles['high'].max()
                                    break

                        delta_next = next_candles['high'].max() - next_candles['low'].min() if not next_candles.empty else None

                        col_g = first_extreme - first_open_price if first_open_price is not None else None
                        col_h = second_extreme - first_open_price if first_open_price is not None else None

                        results.append([
                            len(results) + 1,  # Row number of the result
                            delta,             # Delta of three rows
                            first_open_price,  # First open price after three candles
                            first_extreme,     # First extreme (max or min of the next 5 rows)
                            second_extreme,    # Second extreme (the other value)
                            delta_next,        # Delta of the next five rows
                            col_g,             # Column G: (D - C)
                            col_h              # Column H: (E - C)
                        ])

                    # Jump to the next 8 rows
                    i += 8

                # Create a DataFrame for the results
                results_df = pd.DataFrame(results, columns=[
                    'Row Number', 'Delta (Max-Min)', 'First Open Price',
                    'First Extreme', 'Second Extreme', 'Delta (Next 5 Rows)', 'Column G (D-C)', 'Column H (E-C)'
                ])

                # Calculate I2, I3, I4 values
                i2 = results_df['Column G (D-C)'].gt(1).sum()
                i3 = results_df['Column G (D-C)'].lt(-1).sum()
                i4 = i2 / i3 if i3 != 0 else None

                # Append I4 value to the condition's ratios
                condition_ratios.append(i4 if i4 is not None else 0)

                # Write the results to the respective sheet in the Excel file
                sheet_name = f"ValueA_{value_a}_Sheet{sheet_num + 1}"
                results_df.to_excel(writer, sheet_name=sheet_name, index=False)

            # Append the summarized ratios for this condition
            summaries.append(f"{value_a}: {condition_ratios}")

    # Write summary to the text file
    with open(summary_file, "w") as summary:
        summary.write("\n".join(summaries))

# Example usage
analyze_xauusd_data('XAUUSD.csv', 'result.xlsx', 'summary.txt')
