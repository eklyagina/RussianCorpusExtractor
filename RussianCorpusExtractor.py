#!/usr/bin/env python
# coding: utf-8

# RussianCorpusExtractor
#      
# This is a program that extracts all the examples (from all the search pages) from a National Russian Corpus fitting an inquiry.
# As an input give the link to the FIRST page (it won't work if you use the other page), the number of pages and the name of the output file.
# As an output you will get take the file with three columns: the text of the examples, the info about the name and the author, the date.
# made by Evgenia Klyagina, https://github.com/eklyagina

# Function RussianCorpusExtractor

# In[73]:


import re
import urllib.request
import pandas as pd 
from tqdm import tqdm
import pprint
def RussianCorpusExctractor(number_of_pages, output_file_name, url):
    texts = []
    dates = []
    info = []
    #search all the pages
    for page in tqdm(range(3)): #number_of_pages-1)):
        final_examples = []
        info_dates = []
        #open the link
        req = urllib.request.Request(url+ "&p=" + str(page))
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
        #extract the examples
        regEx = re.compile('<!--  trim_up.html end -->.*?<!--  homonymy.html start -->', flags= re.DOTALL)
        examples = regEx.findall(html)
        #delete rubish
        regTag = re.compile('<.*?>', re.DOTALL)
        for ex in examples:
            clean_ex = regTag.sub("", ex)
            clean_ex = clean_ex.replace("\n", "")
            clean_ex = re.sub("\s+", " ", clean_ex)
            final_examples.append(clean_ex)
        #split the example into text and info_dates
        for ex in final_examples:
            final_ex = ex.split("[")
            text = final_ex[0]
            #to be sure that phrases like "на том [берегу]" are not parsed like "info" or "date"
            for phrase in final_ex[1:]:
                res = re.search("\d\d\d\d", phrase)
                if res:
                    info_dates.append(phrase)
                    #to work with it later
                else:
                    text = final_ex[0] + "["  + phrase
            texts.append(text)   
        #extract information about the date from the "info_dates"
        for i in range(len(info_dates)):
            res = re.search("\d\d\d\d-\d\d\d\d", info_dates[i])
            #date and unwelcomed punctuation
            pattern = ",?\s+\(?\d\d\d\d-\d\d\d\d\)?]?"
            if not res:
                res = re.search("\d\d\d\d", info_dates[i])
                #date and unwelcomed punctuation
                pattern = ",?\s+\(?\d\d\d\d\)?]?"
            dates.append(res.group())
            info.append(re.sub(pattern, "", info_dates[i])) # remove found date(s)
    #make a table
    data = pd.DataFrame({
        "texts": texts ,
        "info": info,
        "dates": dates,
    })
    print(data)
    return data.to_csv(output_file_name+".csv", encoding='utf-8-sig')


# In[75]:


#Check whether the function works


# In[76]:


RussianCorpusExctractor(3, "pryg", 'https://processing.ruscorpora.ru/search.xml?env=alpha&api=1.0&mycorp=&mysent=&mysize=&mysentsize=&dpp=&spp=&spd=&mydocsize=&mode=main&lang=ru&sort=i_grtagging&nodia=1&text=lexform&req=%D0%BF%D1%80%D1%8B%D0%B3')

