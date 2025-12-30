"""
Script to process Soul Foods transaction data.
Filters for Pink Morsels and calculates total sales (quantity * price).
Outputs a single CSV with Sales, Date, Region columns.
"""

import pandas as pd
import os

def process_csv_files():
    # List of input CSV files
    data_dir = 'data'
    csv_files = [
        os.path.join(data_dir, 'daily_sales_data_0.csv'),
        os.path.join(data_dir, 'daily_sales_data_1.csv'),
        os.path.join(data_dir, 'daily_sales_data_2.csv')
    ]
    
    # Read and combine all CSV files
    dataframes = []
    for file in csv_files:
        df = pd.read_csv(file)
        dataframes.append(df)
    
    # Concatenate all dataframes
    combined_df = pd.concat(dataframes, ignore_index=True)
    
    # Filter for Pink Morsels only (case-insensitive)
    pink_morsels_df = combined_df[combined_df['product'].str.lower() == 'pink morsel']
    
    # Clean the price column (remove $ sign) and convert to float
    pink_morsels_df = pink_morsels_df.copy()
    pink_morsels_df['price'] = pink_morsels_df['price'].str.replace('$', '', regex=False).astype(float)
    
    # Calculate sales (quantity * price)
    pink_morsels_df['sales'] = pink_morsels_df['quantity'] * pink_morsels_df['price']
    
    # Select only the required columns and rename for output
    output_df = pink_morsels_df[['sales', 'date', 'region']].copy()
    output_df.columns = ['Sales', 'Date', 'Region']
    
    # Write to output file
    output_file = os.path.join(data_dir, 'formatted_output.csv')
    output_df.to_csv(output_file, index=False)
    
    print(f"Processing complete!")
    print(f"Total records processed: {len(combined_df)}")
    print(f"Pink Morsel records: {len(pink_morsels_df)}")
    print(f"Output saved to: {output_file}")
    print(f"\nSample output:")
    print(output_df.head(10))

if __name__ == '__main__':
    process_csv_files()
