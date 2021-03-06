# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1iaI_t5NURXnonQjUpUEfXJkDASho3vCs
"""

import numpy as np 
import pandas as pd

df_meta = pd.read_csv("/content/movies_metadata.csv")
df_meta.columns

df_meta = df_meta[['id', 'genres', 'original_language', 'production_countries', 'tagline', 'original_title', 'adult', 'release_date', 'status']]
df_meta.status.unique()

for i in range(len(df_meta)):
    tmp = df_meta['status'][i]
    if (tmp == "Released"):
        df_meta['status'][i] = "Released"
    else:
        df_meta['status'][i] = ''

import json
import ast
df_meta['genres'][0]

for i in range(len(df_meta['genres'])):
    str_tmp = ""
    genre = df_meta['genres'][i]
    genre = str(genre).strip("'<>() ").replace('\'', '\"')
    json_genre = json.loads(genre)
    for j in range(len(json_genre)):
        str_tmp += (json_genre[j]['name'])+" "
    df_meta['genres'][i] = str_tmp

df_meta['genres'][0]

df_meta['production_countries'][0]

df_meta['production_countries'].replace(np.nan, '', inplace=True)
for i in range(len(df_meta['production_countries'])):
    str_tmp = ""
    country = df_meta['production_countries'][i]
    if (country != ''):
        country = json.dumps(ast.literal_eval(country))
        json_country = json.loads(country)
    
        try:
            for j in range(len(json_country)):
                str_tmp += (json_country[j]['name'])
            #print(str_tmp)
            
            df_meta['production_countries'][i] = str_tmp
        except:
            print("Error")
    else:
        print("Blank")

df_meta['production_countries'][0:3]

df_keyword = pd.read_csv('/content/keywords.csv')

df_keyword['keywords'][0]

df_keyword['keywords'][1]

for i in range(len(df_keyword['keywords'])):
    str_tmp = ""
    keyword = df_keyword['keywords'][i]
    keyword = json.dumps(ast.literal_eval(keyword))
    json_keyword = json.loads(keyword)
    
    for j in range(len(json_keyword)):
        str_tmp += (json_keyword[j]['name'])+" "
        
    df_keyword['keywords'][i] = str_tmp

df_keyword['keywords'][0]

df_keyword['keywords'][1]

df_meta['id']=df_meta['id'].astype(str)
df_keyword['id']=df_keyword['id'].astype(str)
df_merge = pd.merge(df_keyword, df_meta, on='id', how='inner')[['id', 'genres', 'original_language', 'production_countries', 'tagline', 'original_title', 'adult', 'release_date', 'status', 'keywords']]

df_merge['keywords'].replace('', np.nan, inplace=True)
df_merge['genres'].replace('', np.nan, inplace=True)
df_merge['original_title'].replace('', np.nan, inplace=True)

df_merge.to_csv('filter_data.csv')

df=pd.read_csv('filter_data.csv')

def combine_features(row):
    return str(row['original_title'])+' '+str(row['genres'])+' '+str(row['keywords'])+' '+str(row['production_countries'])

df['combined_value'] = df.apply(combine_features, axis = 1)

df['index'] = [i  for i in range(0, len(df))]

def title(index):
    return df[df.index == index]["original_title"].values[0]

def index(original_title):
    return df[df.original_title == original_title]["index"].values[0]

!pip3 install -U sentence-transformers

pip install tqdm boto3 requests regex sentencepiece sacremoses

from sentence_transformers import SentenceTransformer
bert = SentenceTransformer('bert-base-nli-mean-tokens')

sentence_embeddings = bert.encode(df['combined_value'].tolist())

pip install -U scikit-learn scipy matplotlib

from sklearn.metrics.pairwise import cosine_similarity
similarly = cosine_similarity(sentence_embeddings)

movie_name = input('')
movie_recommendation = sorted(list(enumerate(similarly[index(movie_name)])), key = lambda x:x[1], reverse = True)
print(title(movie_recommendation[1][0]), (movie_recommendation[2][0]), (movie_recommendation[3][0]))