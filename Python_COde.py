# -*- coding: utf-8 -*-
"""Black_Coffer.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Dmqq3U3ZrDaDuHT6iTNgg8B8dgIU54gs
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
nltk.download('punkt')
nltk.download('stopwords')
import re

from google.colab import drive
drive.mount('/content/drive')

# from google.colab import drive
# drive.mount('/gdrive')

stopwords_dir = "/content/drive/MyDrive/20211030 Test Assignment (1)/StopWords"

stopwords= set()
for files in os.listdir(stopwords_dir):
  with open(os.path.join(stopwords_dir,files),'r',encoding='ISO-8859-1') as f:
    stopwords.update(set(f.read().splitlines()))

df= pd.read_excel("/content/drive/MyDrive/20211030 Test Assignment (1)/Input.xlsx")

df

allfiles=[]



for index, row in df.iterrows():
  url = row['URL']
  url_id = row['URL_ID']
  # print(url,url_id)
  header = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"}
  try:
    response = requests.get(url,headers=header)
    # print(response)
  except:
    print("can't get response of {}".format(url_id))
  try:
    soup = BeautifulSoup(response.content, 'html.parser')
    # print(soup)
  except:
    print("can't get page of {}".format(url_id))
  try:
    title = soup.find('h1').get_text()
    # print(title)
  except:
    print("can't get title of {}".format(url_id))
    continue
  #find text
  article = ""
  try:
    for p in soup.find_all('p'):
      article += p.get_text()
    seostring="Ranking customer behaviours for business strategyAlgorithmic trading for multiple commodities markets, like Forex, Metals, Energy, etc.Trading Bot for FOREXPython model for the analysis of sector-specific stock ETFs for investment purposesPlaystore & Appstore to Google Analytics (GA) or Firebase to Google Data Studio Mobile App KPI DashboardGoogle Local Service Ads LSA API To Google BigQuery to Google Data StudioAI Conversational Bot using RASARecommendation System ArchitectureRise of telemedicine and its Impact on Livelihood by 2040Rise of e-health and its impact on humans by the year 2030Rise of e-health and its impact on humans by the year 2030Rise of Chatbots and its impact on customer support by the year 2040AI/ML and Predictive ModelingSolution for Contact Centre ProblemsHow to Setup Custom Domain for Google App Engine Application?Code Review ChecklistRanking customer behaviours for business strategyAlgorithmic trading for multiple commodities markets, like Forex, Metals, Energy, etc.Trading Bot for FOREXPython model for the analysis of sector-specific stock ETFs for investment purposesPlaystore & Appstore to Google Analytics (GA) or Firebase to Google Data Studio Mobile App KPI DashboardGoogle Local Service Ads LSA API To Google BigQuery to Google Data StudioAI Conversational Bot using RASARecommendation System ArchitectureRise of telemedicine and its Impact on Livelihood by 2040Rise of e-health and its impact on humans by the year 2030Rise of e-health and its impact on humans by the year 2030Rise of Chatbots and its impact on customer support by the year 2040AI/ML and Predictive ModelingSolution for Contact Centre ProblemsHow to Setup Custom Domain for Google App Engine Application?Code Review Checklist marketsforex metals energy ga markets forex metals energy ga checklist"
    sublist=[word for word in seostring.split()]
    pattern = '|'.join(map(re.escape, sublist))
    article = re.sub(r'\b(?:{})\b'.format(pattern), '', article)
    article = article.lower()
    allfiles.append(article)
    # print(article)
    # article = re.sub(r"(@\[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?|[\w\.-]+@[\w\.-]+',", "", article)
    article = " ".join([word for word in word_tokenize(article) if word not in (stopwords)])
    # print(article)
    filename = '/content/drive/MyDrive/20211030 Test Assignment (1)/AllFiles/' + str(url_id) + '.txt'
    print(filename)
    with open(filename, 'w') as file:
      file.write(title + '\n' + article)
    # print(title)
    # print(article)
    article = ""
    
  except:
    print("can't get text of {}".format(url_id))

positive= set()
negative = set() 
master_dir="/content/drive/MyDrive/20211030 Test Assignment (1)/MasterDictionary"
for files in os.listdir(master_dir):
  # print(files)
  with open(os.path.join(master_dir,files),'r',encoding='ISO-8859-1') as f:
    if files=="positive-words.txt":
      positive.update(set(f.read().splitlines()))
    else:
      negative.update(set(f.read().splitlines()))

print(len(positive),len(negative))

pos_score,neg_score,polar_score,subject_score=[],[],[],[]

textfiles = "/content/drive/MyDrive/20211030 Test Assignment (1)/AllFiles"

for files in os.listdir(textfiles): 
  print(files)
  with open(os.path.join(textfiles,files),'r',encoding='ISO-8859-1') as f:
     text=f.read()
     words = word_tokenize(text) 
     pos,neg=0,0
    #  print(words)
  for i in words:
       if i in positive:
         pos+=1 
       elif i in negative:
         neg+=1 
      #  if i==".":
      #    sentence_count+=1  
  pos_score.append(pos)
  neg_score.append(neg)
  polar=(pos-neg)/((pos+neg)+0.000001)
  polar_score.append(polar)

print(pos_score)
print(neg_score)

print(min(polar_score))
print(max(polar_score))

def syllable_count(word):
    count = 0
    vowels = "aeiouy"
    if word[0] in vowels:
        count += 1
    for index in range(1, len(word)):
        if word[index] in vowels and word[index - 1] not in vowels:
            count += 1
    if word.endswith("e"):
        count -= 1
    if count == 0:
        count += 1
    return count

avg_sen_len,percentage_complex,fog_index,avg_num_word_sen=[],[],[],[]
complex_word_count=[]
syllable_per=[]
avg_word_length=[]

count=0
for files in os.listdir(textfiles): 
  print(files)
  with open(os.path.join(textfiles,files),'r',encoding='ISO-8859-1') as f:
     text=f.read()
     sentences = text.split('.')
     sen_count=len(sentences)
     text=re.sub(r"(@\[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?|[\w\.-]+@[\w\.-]+',", "", text)
     words = [word  for word in text.split()] 
     word_count=len(words)
     vowels={"a","e","i","o","u"}
     complex_words=0
     syllablecountforcol=0
     avgcharlength=0 
     for word in words:
      if syllable_count(word) > 2:
        complex_words+=1 
      # avgcharlength+=sum(1 for letter in word.split())
      avgcharlength += len(word)
      syllablecountforcol+=syllable_count(word) 
  syllable_per.append(syllablecountforcol/word_count)
  avg_word_length.append(avgcharlength/word_count) 
  complex_word_count.append(complex_words)
  avg_sen_len.append(word_count/sen_count)
  percentage_complex.append(complex_words/word_count)
  fog_index.append(avg_sen_len[-1]/sen_count)
  subject_score.append((pos_score[count]+neg_score[count])/(word_count+0.000001))

word_count_col=[]

def count_personal_pronouns(text):
    personal_pronouns = ["I", "we", "my", "ours", "us","We","My","Ours","i"]
    count = 0
    for pronoun in personal_pronouns:
      count += len(re.findall(r"\b" + pronoun + r"\b", text)) 
    print(count)
    return count

pronoun_count=[]
total_word_count=[]

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
nltk.download('punkt')
nltk.download('stopwords')
stop = stopwords.words('english')
for files in os.listdir(textfiles): 
   with open(os.path.join(textfiles,files),'r',encoding='ISO-8859-1') as f:
    text=f.read()
    personal_pronouns = ["I", "we", "my", "ours", "us","We","My","Ours","i"]
    count = 0
    for pronoun in personal_pronouns:
      count += len(re.findall(r"\b" + pronoun + r"\b", text)) 
    pronoun_count.append(count)
    print(count)
    text=text.lower()
    text = re.sub(r"(@\[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?", "", text)
    count = sum(1 for word in text.split() if word not in (stop))
    total_word_count.append(count)

print(pronoun_count)
print(total_word_count)

output= pd.read_excel("/content/drive/MyDrive/20211030 Test Assignment (1)/Output Data Structure.xlsx")
output

output.drop([44-37,57-37,144-37], axis = 0, inplace=True)

len(output)

variables = [pos_score,
            neg_score,
            polar_score,
            subject_score,
            avg_sen_len,
            percentage_complex,
            fog_index,
            avg_sen_len,
            complex_word_count,
            total_word_count,
            syllable_per,
            pronoun_count,
            avg_word_length]

for i in variables:
  print(len(i))

for i, var in enumerate(variables):
  output.iloc[:,i+2] = var

output.to_csv('/content/drive/MyDrive/20211030 Test Assignment (1)/Output.csv')

output

