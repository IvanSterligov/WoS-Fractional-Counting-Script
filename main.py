import pandas as pd
import re
from tqdm import tqdm

tqdm.pandas() #добавляем индикатор выполнения

df = pd.read_csv(r'c:\ivan\savedrecs.txt', sep='\t', header=0, index_col=False) #загружаем полученные из WoS данные (если слеплены из многих файлов, нужно до или после скрипта убрать повторяющиеся строки с заголовками)
df['author_count']='' #создаем пустую колонку для числа авторов
df['affil_count']='' #и для числа уникальных аффилиаций
df['affil_names']='' # для списка аффилиаций
print ('loaded publications:', len(df.index)) 
print ('starting processing...')

match=['State Univ HSE','Natl Res Univ HSE','HSE, Moscow, Russia','GU HSE','NRU HSE','HSE Univ', 'High Sch Econ','Higher Sch Econ','Higher, Sch Econ'] #сюда вносим список вариантов написания аффилиации, case-dependent 

def fracount (data):
    counter = 0 #эта переменная будет хранить совокупную долю по аффилиации, которую в конце разделим на число авторов

    rawnames = data['AF'] #загружаем список имен авторов
    if rawnames == '': return 'no author names' #если нет авторов, вместо доли возвращаем сообщение об ошибке 
    lnames=rawnames.split(';') #получаем список имен авторов
    lnames = [x.strip(' ') for x in lnames] #убираем лишние пробелы
    acount = len(lnames) #считаем число авторов
    df['author_count'][data.name]=acount #вносим число авторов в соотв. колонку 
    
    rawaffils = data['C1']  #загружаем список аффилиаций
    if rawaffils == '': return 'no affiliations'  #если нет аффилиаций, вместо доли возвращаем сообщение об ошибке
    rawaffils_noauthors=re.sub(r'[[][^]]*[]]', '', rawaffils).strip() #убираем имена авторов из C1 (в []) для выгрузки списка аффилиаций, затем убираем лишние пробелы
    df['affil_names'][data.name]=rawaffils_noauthors #выгружаем список аффилиаций

    laffils=rawaffils.split('; [') #получаем список аффилиаций и приписанных к ним авторов

    affcount=len(laffils) #cчитаем число уникальных аффилиаций
    df['affil_count'][data.name]=affcount #вносим предварительно число аффилиаций в соотв. колонку
    
    if affcount == 1: #случай, когда одна аффилиация
        if ';' in rawaffils_noauthors: df['affil_count'][data.name]='possibly bad affiliation' #если битая аффилиация (все аффилиации слиплись в одну) вместо числа аффилиаций указываем на ошибку
        if any(x in rawaffils for x in match):  #проверяем, есть ли наша аффилиация, если да, доля = 1, иначе = 0
            return 1
        else:
            return 0
           
    for x in lnames:   #цикл подсчета доли для каждого отдельного автора
            thisaffillist=[] #сюда складываем аффилиации данного автора
            a_affilcount=sum(x in y for y in laffils) #считаем число аффилиаций на автора            
            for y in laffils: #составляем список всех аффилиаций данного автора
                if x in y:
                    thisaffillist.append(y)
            for x in match: #считаем долю за данного автора для всех вариантов аффилиаций
                for y in thisaffillist:
                    if x in str(y):                        
                        counter = counter+(1/a_affilcount)
                        thisaffillist.remove(y) #чтобы избежать двойного учета, если совпадет с другим вариантом написания аффилиации
    return counter/acount #подсчитываем и возвращаем долю

df['share'] = df.progress_apply(fracount, axis=1)
print ('saving to c:\Ivan\savedrecs.csv and c:\Ivan\savedrecs.xlsx...')
df.to_csv((r'c:\Ivan\savedrecs.csv'), sep='\t')
df.to_excel(r'c:\Ivan\savedrecs.xlsx')
print ('... done')  
