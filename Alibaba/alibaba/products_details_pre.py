import pandas as pd

products_preprocessed = pd.read_csv(r'C:\Users\sudil\Desktop\ML_Projects\Web_scraping\Alibaba\alibaba\Product_Details_2.csv',index_col=False)
# remove null
products_preprocessed = products_preprocessed.dropna(axis=0,how="all")
products_preprocessed.to_csv('Product_Details_Processed_2.csv',index=False)