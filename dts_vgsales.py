import pandas as pd

df = pd.read_csv('vgsales.csv', index_col='Rank')
df = df.astype({'Year': 'Int32'})

df.rename(columns={'EU_Sales':'SalesInEurope', 'JP_Sales': 'SalesInJapan'}, inplace = True)

year_and_genre_filter = ((df['Year'] > 2016) | (df['Genre'] =='Shooter'))
df = df.loc[year_and_genre_filter]

print('----------------------------------->')

sales_regions = ['SalesInEurope', 'SalesInJapan', 'Global_Sales', 'NA_Sales', 'Other_Sales']

for sales_region in sales_regions:
    print(f"Sum of sales amount of {sales_region} : ${df[sales_region].sum():,.2f}")
    print(f"Count of sales of {sales_region} : ${df[sales_region].count():,.2f}")
    print(f"Average sales amount of {sales_region} : ${df[sales_region].mean():,.2f}")
    print(f"Median sales amount of {sales_region} : ${df[sales_region].median():,.2f}")
    print(f"Standard deviation of sales amount of {sales_region} : ${df[sales_region].std():,.2f}")
    print('----->')
    


