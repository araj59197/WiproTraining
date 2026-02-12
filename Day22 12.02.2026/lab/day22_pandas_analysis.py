import pandas as pd
import numpy as np

def analyze_sales_data():
    try:
        df = pd.read_csv('sales.csv')
        
        print("Sales Data Loaded Successfully:")
        print(df)
        
        df['Total'] = df['Quantity'] * df['Price']
        print("\nDataFrame with 'Total' column:")
        print(df)
        
        total_sales_dates = df.groupby('Date')['Total'].sum().values
        
        total_sales = np.sum(total_sales_dates)
        average_daily_sales = np.mean(total_sales_dates)
        std_dev_sales = np.std(total_sales_dates)
        
        print("\nSales Statistics (using NumPy):")
        print(f"Total Sales: {total_sales}")
        print(f"Average Daily Sales: {average_daily_sales}")
        print(f"Standard Deviation of Daily Sales: {std_dev_sales:.2f}")
        
        product_sales = df.groupby('Product')['Quantity'].sum()
        best_selling_product = product_sales.idxmax()
        total_quantity_sold = product_sales.max()
        
        print(f"\nBest-selling product: {best_selling_product} (Quantity: {total_quantity_sold})")

    except FileNotFoundError:
        print("Error: 'sales.csv' file not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    analyze_sales_data()
