RussianCorpusExtractor
     
This is a program that extracts all the examples (from all the search pages) from a National Russian Corpus fitting an inquiry.
As an input give the link to the FIRST page (it won't work if you use the other page), the number of pages and the name of the output file.
As an output you will get take the file with three columns: the text of the examples, the info about the name and the author, the date.
made by Evgenia Klyagina, https://github.com/eklyagina

Function RussianCorpusExtractor


```python
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
```


```python
#Check whether the function works
```


```python
RussianCorpusExctractor(3, "pryg", 'https://processing.ruscorpora.ru/search.xml?env=alpha&api=1.0&mycorp=&mysent=&mysize=&mysentsize=&dpp=&spp=&spd=&mydocsize=&mode=main&lang=ru&sort=i_grtagging&nodia=1&text=lexform&req=%D0%BF%D1%80%D1%8B%D0%B3')
```

    100%|████████████████████████████████████████████████████████████████████████████████████| 3/3 [00:01<00:00,  1.95it/s]

                                                    texts  \
    0   :)) Да какой жираф! Всем жирафам жираф… :))) П...   
    1       Гости пришли, а он прыг на потолок и молчок!    
    2       Близко-близко подполз да как прыгнет — прыг!    
    3    А Котофей Котофеич прыг с кроватки да тихоньк...   
    4    Наконец встал, прыг-прыг к двери, на пороге о...   
    5    Вот он раз и дождался у дороги версты три за ...   
    6   А он прыг на форточку, а там четырнадцатый этаж.    
    7                Она с тумбочки прыг и покорно идет.    
    8   Через игру научила командам «лежать», «сидеть»...   
    9   Девочки уже раздали автографы и явно скучали ―...   
    10   ― Пупарас Трыг ― мое сердце прыг, ― пробормот...   
    11  Но, правда, и резво скачущая: прыг-скок со стр...   
    12  В бурьян приткнёт, за бочку засунет, а он ― ко...   
    13  А добрый молодец сразу прыг в кусты, и только ...   
    14  Опасные, но притупленные сумерками лезвия осок...   
    15  Он держит скользкую удочку. И вдруг она резко ...   
    16  Я себе коньяку рюмку ― буль-буль-буль, книжку ...   
    17  Я и смекнуть не успел, старший Петька пошурова...   
    18  Такой ядреный, что с каждым глотком сердце ― п...   
    19  Так, не прыжок даже, а совсем малюсенький прыг...   
    20  Без всяких марок и штемпелей ― прыг ― и уже у ...   
    21  Уже убегала, а браслет прыг из рук ― и закатил...   
    22   «Представьте себе на минуту ― приезжает челов...   
    23  А я, бля, не будь дурак, тоже из канцелярии ― ...   
    24  Однажды он наружу прыг― И что, представьте, ви...   
    25   (Осталась ли ты? почерневшая душонка? ПРЫГ-СК...   
    26  Стал корешки жечь, по бубну стучать, потом опя...   
    27  Водитель ― усатый дядька ― не спеша, роется в ...   
    28  Пипе и Тане строжайше запрещено было даже случ...   
    29  Прыг-скок Кошки плохо поддаются дрессировке. З...   
    30   ― Он подарил мне помаду, которую по телевизор...   
    31  Прыг-скок через мосток, через бугорок, через в...   
    32  Очередной небольшой секрет откроет лингвист, п...   
    33  В комедии Грибоедова Фамусов распекает дочку: ...   
    34  Толк чем? ― ногой. Прыг откуда? ― из постели. ...   
    35  Прыгать полагается так: держась за ручки, став...   
    36  То есть приманил по первоначалу ― ногтем поскр...   
    37  Как посмотрит на него чужой человек, так он пр...   
    
                                                     info      dates  
    0                                 Запись LiveJournal        2004  
    1    Георгий Юдин. Васильковое варенье // «Мурзилка»        2003  
    2                Е. И. Чарушин. Тюпа, Томка и сорока        1946  
    3                               А. М. Ремизов. Зайка        1905  
    4                         И. С. Тургенев. Живые мощи        1874  
    5              М. Ю. Лермонтов. Герой нашего времени   1839-1841  
    6         Сергей Шикера. Египетское метро // «Волга»        2016  
    7                      Сергей Носов. Фигурные скобки        2015  
    8   Диана Злобина. Зачем ученые лис приручили // «...       2014  
    9                          Виктор Пелевин. S.N.U.F.F        2011  
    10                         Виктор Пелевин. S.N.U.F.F        2011  
    11              Борис Евсеев. Евстигней // «Октябрь»        2010  
    12              В. Г. Галактионова. Спящие от печали        2010  
    13  В. И. Букур, Н. В. Горланова. Моя тихая радост...       2009  
    14                            Сергей Шаргунов. Обман        2009  
    15                            Сергей Шаргунов. Обман        2009  
    16              Татьяна Соломатина. Акушер-ХА! Байки        2009  
    17  Александр Иличевский. Бутылка // «Зарубежные з...       2005  
    18  Александр Иличевский. Бутылка // «Зарубежные з...       2005  
    19    Татьяна Сахарова. Добрая фея с острыми зубками        2005  
    20           Михаил Шишкин. Венерин волос // «Знамя»        2004  
    21           Михаил Шишкин. Венерин волос // «Знамя»        2004  
    22  Феликс Кузнецов. Шолохов и «анти-Шолохов» // «...       2004  
    23  Александр Логинов. Мираж // Интернет-альманах ...       2003  
    24           Мария Семенова. Волкодав: Знамение пути        2003  
    25    Олег Гладов. Любовь стратегического назначения   2000-2003  
    26    Олег Гладов. Любовь стратегического назначения   2000-2003  
    27    Олег Гладов. Любовь стратегического назначения   2000-2003  
    28  Дмитрий Емец. Таня Гроттер и магический контра...       2002  
    29   Дмитрий Певцов. Прыг-скок // «Автопилот».12.15]        2002  
    30         Елена и Валерий Гордеевы. Не все мы умрем        2002  
    31  Ирина Григорьева. Помеха справа // «Автопилот»...       2002  
    32  Мария Пупшева. Краткость ― сестра глагола // «...       2002  
    33  Мария Пупшева. Краткость ― сестра глагола // «...       2002  
    34  Мария Пупшева. Краткость ― сестра глагола // «...       2002  
    35  Велопробег в рабочий полдень // «Домовой».10.04]        2002  
    36                           Андрей Измайлов. Трюкач        2001  
    37              Вадим Бурлак. Хранители древних тайн        2001  
    

    
    
