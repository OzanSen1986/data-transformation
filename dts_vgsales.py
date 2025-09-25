import pandas as pd

df = pd.read_csv('vgsales.csv')

# short summary
print(df.columns)
print(f"Total number of sales rows: {df['EU_Sales'].count()}")