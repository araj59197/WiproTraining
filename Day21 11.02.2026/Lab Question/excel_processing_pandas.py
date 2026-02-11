import pandas as pd
df = pd.read_excel('sales_data.xlsx', sheet_name='2025')
df['Total'] = df['Quantity'] * df['Price']
print("Updated DataFrame:")
print(df)
df.to_excel('sales_summary.xlsx', index=False)

print("\nData successfully saved to sales_summary.xlsx")
