import pandas as pd

df = pd.read_csv('vgsales.csv', index_col='Rank')
df = df.astype({'Year': 'Int32'})

df.rename(columns={'EU_Sales':'SalesInEurope', 'JP_Sales': 'SalesInJapan'}, inplace = True)

year_and_genre_filter = ((df['Year'] > 2016) | (df['Genre'] =='Shooter'))
df = df.loc[year_and_genre_filter]

print('----------------------------------->')

print(f"Sales Amount of Europe : ${df['SalesInEurope'].sum():,.2f}")
print(f"Sales Amount of Japan : ${df['SalesInJapan'].sum():,.2f}")
print(f"Sales Amount of Global Sales: ${df['Global_Sales'].sum():,.2f}")
print(f"Sales Amount of NA Sales: ${df['NA_Sales'].sum():,.2f}")
print(f"Sales Amount of Other Sales: ${df['Other_Sales'].sum():,.2f}")

