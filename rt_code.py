# start with dataframe amazon data 
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#amazon_data
# Histogram data for entire population in the category
hist_data = amazon_data.loc[:,['category','overall']]
hist_data_electronics = hist_data.loc[hist_data['category']=='Electronics']
electronics_ls = hist_data_electronics['overall'].values
hist_data_cds = hist_data.loc[hist_data['category']=='CDs and Vinyl']
cds_ls = hist_data_cds['overall'].values
hist_data_books = hist_data.loc[hist_data['category']=='Books']
books_ls = hist_data_books['overall'].values

plt.figure()
graph_electronics = hist_data_electronics.plot.hist(alpha=0.5,bins=5,color='blue')
graph_cds = hist_data_cds.plot.hist(alpha=0.5,bins=5,color='red')
graph_books = hist_data_books.plot.hist(alpha=0.5,bins=5,color='green')

books = amazon_data[amazon_data['category'] == 'Books']
cds = amazon_data[amazon_data['category'] == 'CDs and Vinyl']
electronics = amazon_data[amazon_data['category'] == 'Electronics']
# Extract "honest review" population
books = hist_data_books.dropna(axis=0,how='any',subset=['reviewText'])
cds = hist_data_cds.dropna(axis=0,how='any',subset=['reviewText'])
electronics = hist_data_electronics.dropna(axis=0,how='any',subset=['reviewText'])

incent_books = books[books['reviewText'].str.contains('unbiased review|honest review')]
incent_cds = cds[cds['reviewText'].str.contains('unbiased review|honest review')]
incent_electronics = electronics[electronics['reviewText'].str.contains('unbiased review|honest review')]

ratings = [1, 2, 3, 4, 5]
rating_hist_books = incent_books.groupby('overall').count()['asin']
plt.bar(ratings,rating_hist_books,color='blue',alpha=0.5)
plt.title('"Honest" Book review')

rating_hist_cds = incent_cds.groupby('overall').count()['asin']
plt.bar(ratings,rating_hist_cds,color='red',alpha=0.5)
plt.title('"Honest" CDs review')

rating_hist_elect = incent_electronics.groupby('overall').count()['asin']
plt.bar(ratings,rating_hist_elect,color='green',alpha=0.5)
plt.title('"Honest" Electronics review')