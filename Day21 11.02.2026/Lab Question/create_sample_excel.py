import pandas as pd

data = {
    'Product': ['A', 'B', 'C'],
    'Quantity': [10, 20, 15],
    'Price': [50, 30, 40]
}

df = pd.DataFrame(data)
df.to_excel('sales_data.xlsx', sheet_name='2025', index=False)

print("Sample Excel file 'sales_data.xlsx' created successfully!")
print("\nData:")
print(df)
