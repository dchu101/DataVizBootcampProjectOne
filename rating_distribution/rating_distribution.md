

```python
import pandas as pd
import numpy as np
import ast 
import json
import time
import matplotlib.pyplot as plt
```


```python
#makes a data frame of the reviews, minus the books
no_books_reviews_df = pd.read_csv('reviews (no books).csv')
```


```python
#Generates a list of all book review files names
book_prefix='Book Reviews/reviews_books_'
book_review_files = []

for file_no in range(1,3001):
    book_review_files.append(book_prefix + str(file_no).zfill(4) + '.csv')
```


```python
#Generates a list of data frames to concatenate
i = 0
book_concat_list=[]
for file in book_review_files:
    df = pd.read_csv(file)
    book_concat_list.append(df)
    i += 1    
    #if i % 100 == 0:
        #print(file)
```


```python
#Concats a single book reviews dataframe
book_reviews_df = pd.concat(book_concat_list)
book_reviews_df['category'] = 'Books'
```


```python
#concats books and no books review dataframes
concat_list = [no_books_reviews_df, book_reviews_df]
all_reviews = pd.concat(concat_list)
```


```python
#creates list of all file names containing the meta data
meta_list = []
prefix='Metadata/meta_Books_file'
for file_no in range(1,35):
    meta_list.append(prefix + str(file_no).zfill(4) + '.csv')
#CDs
prefix='Metadata/meta_CDs_and_Vinyl_file'
for file_no in range(1,6):
    meta_list.append(prefix + str(file_no).zfill(4) + '.csv')
```


```python
#concats a list of smaller metadata datafames
meta_concat_list=[]
for file in meta_list:
    df = pd.read_csv(file)
    meta_concat_list.append(df)
```


```python
#concats a single metadata dataframe, de-dupes
meta_df = pd.concat(meta_concat_list)
#print(len(meta_df))
meta_df.drop_duplicates(inplace=True)
#print(len(meta_df))
```


```python
#merges the reviews df with the metadata df
amazon_data = all_reviews.merge(meta_df, how='left', left_on='asin', right_on='ASIN')
```


```python
#Drop 'ASIN' from the right column
#Some reviews will still have no metadata
amazon_data = amazon_data.drop('ASIN', axis=1)
```


```python
books = amazon_data[amazon_data['category'] == 'Books']
cds = amazon_data[amazon_data['category'] == 'CDs and Vinyl']
electronics = amazon_data[amazon_data['category'] == 'Electronics']

books = books.dropna(axis=0,how='any',subset=['reviewText'])
cds = cds.dropna(axis=0,how='any',subset=['reviewText'])
electronics = electronics.dropna(axis=0,how='any',subset=['reviewText'])

incent_books = books[books['reviewText'].str.contains('unbiased review|honest review')]
incent_cds = cds[cds['reviewText'].str.contains('unbiased review|honest review')]
incent_electronics = electronics[electronics['reviewText'].str.contains('unbiased review|honest review')]
    
def review_distribution_plot(df):
    
    ratings = [1, 2, 3, 4, 5]
    rating_hist = df.groupby('overall').count()['asin']
    
    #plt.title(f'{df.iloc[0,1]} Review Distribution')
    plt.bar(ratings, rating_hist)
```


```python
ratings = [1, 2, 3, 4, 5]
rating_hist_books = incent_books.groupby('overall').count()['asin']
plt.bar(ratings,rating_hist_books,color='blue',alpha=0.5)
plt.title('"Honest" Book review')
```




    Text(0.5,1,'"Honest" Book review')




![png](output_12_1.png)



```python
rating_hist_cds = incent_cds.groupby('overall').count()['asin']
plt.bar(ratings,rating_hist_cds,color='red',alpha=0.5)
plt.title('"Honest" CDs review')
```




    Text(0.5,1,'"Honest" CDs review')




![png](output_13_1.png)



```python
rating_hist_elect = incent_electronics.groupby('overall').count()['asin']
plt.bar(ratings,rating_hist_elect,color='green',alpha=0.5)
plt.title('"Honest" Electronics review')
```




    Text(0.5,1,'"Honest" Electronics review')




![png](output_14_1.png)



```python
#amazon_data.columns
```


```python
#amazon_data.groupby(['category']).count()
```


```python
hist_data = amazon_data.loc[:,['category','overall']]
```


```python
hist_data_electronics = hist_data.loc[hist_data['category']=='Electronics']
electronics_ls = hist_data_electronics['overall'].values
hist_data_cds = hist_data.loc[hist_data['category']=='CDs and Vinyl']
cds_ls = hist_data_cds['overall'].values
hist_data_books = hist_data.loc[hist_data['category']=='Books']
books_ls = hist_data_books['overall'].values
```


```python
ratings = [1,2,3,4,5] 
graph_electronics = hist_data_electronics.plot.hist(alpha=0.5,bins=5,color='green') 
plt.title('Electronics reviews') 
plt.xticks(ratings) 
plt.show()
```


![png](output_19_0.png)



```python
hist_data_electronics.describe()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>overall</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>1.493863e+06</td>
    </tr>
    <tr>
      <th>mean</th>
      <td>4.237861e+00</td>
    </tr>
    <tr>
      <th>std</th>
      <td>1.177106e+00</td>
    </tr>
    <tr>
      <th>min</th>
      <td>1.000000e+00</td>
    </tr>
    <tr>
      <th>25%</th>
      <td>4.000000e+00</td>
    </tr>
    <tr>
      <th>50%</th>
      <td>5.000000e+00</td>
    </tr>
    <tr>
      <th>75%</th>
      <td>5.000000e+00</td>
    </tr>
    <tr>
      <th>max</th>
      <td>5.000000e+00</td>
    </tr>
  </tbody>
</table>
</div>




```python
graph_cds = hist_data_cds.plot.hist(alpha=0.5,bins=5,color='red')
plt.title('CDs reviews')
plt.xticks(ratings)
plt.show()
```


![png](output_21_0.png)



```python
hist_data_cds.describe()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>overall</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>327759.000000</td>
    </tr>
    <tr>
      <th>mean</th>
      <td>4.412864</td>
    </tr>
    <tr>
      <th>std</th>
      <td>0.982560</td>
    </tr>
    <tr>
      <th>min</th>
      <td>1.000000</td>
    </tr>
    <tr>
      <th>25%</th>
      <td>4.000000</td>
    </tr>
    <tr>
      <th>50%</th>
      <td>5.000000</td>
    </tr>
    <tr>
      <th>75%</th>
      <td>5.000000</td>
    </tr>
    <tr>
      <th>max</th>
      <td>5.000000</td>
    </tr>
  </tbody>
</table>
</div>




```python
graph_books = hist_data_books.plot.hist(alpha=0.5,bins=5,color='blue')
plt.title('Books reviews')
plt.xticks(ratings)
plt.show()
```


![png](output_23_0.png)



```python
hist_data_books.describe()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>overall</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>3.000000e+06</td>
    </tr>
    <tr>
      <th>mean</th>
      <td>4.240870e+00</td>
    </tr>
    <tr>
      <th>std</th>
      <td>1.055278e+00</td>
    </tr>
    <tr>
      <th>min</th>
      <td>1.000000e+00</td>
    </tr>
    <tr>
      <th>25%</th>
      <td>4.000000e+00</td>
    </tr>
    <tr>
      <th>50%</th>
      <td>5.000000e+00</td>
    </tr>
    <tr>
      <th>75%</th>
      <td>5.000000e+00</td>
    </tr>
    <tr>
      <th>max</th>
      <td>5.000000e+00</td>
    </tr>
  </tbody>
</table>
</div>


