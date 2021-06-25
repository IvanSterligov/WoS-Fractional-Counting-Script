import pandas as pd
from tqdm import tqdm

tqdm.pandas() #добавляем индикатор выполнения

df = pd.read_csv(r'c:\ivan\savedrecs.txt', sep='\t', header=0, index_col=False) #загружаем полученные из WoS данные (если слеплены из многих файлов, нужно до или после скрипта убрать повторяющиеся строки с заголовками)
df['author_count']='' #создаем пустую колонку для числа авторов
print ('loaded publications:', len(df.index)) 
print ('starting processing...')

match=['State Univ HSE','Natl Res Univ HSE','HSE, Moscow, Russia','GU HSE','NRU HSE','HSE Univ', 'High Sch Econ','Higher Sch Econ','Higher, Sch Econ'] #сюда вносим список вариантов написания аффилиации, case-dependent 

def fracount (data):
    counter = 0 #эта переменная будет хранить совокупную долю по аффилиации, которую в конце разделим на число авторов
    
    rawaffils = data['C1']  #загружаем список аффилиаций
    
    if rawaffils == '':
        return 'no affiliations'

    laffils=rawaffils.split('; [') #получаем список аффилиаций и приписанных к ним авторов

    affcount=len(laffils) #cчитаем число уникальных аффилиаций

    if affcount == 1: #случай, когда один автор и одна аффилиация
        df['author_count'][data.name]=1 #вносим число авторов в соотв колонку
        if any(x in rawaffils for x in match):  #проверяем, есть ли наша аффилиация, если да, доля = 1, иначе = 0
            return 1
        else:
            return 0
    
    rawnames = data['AF'] #загружаем список имен авторов
     
    if rawnames == '':
        return 'no author names'

    lnames=rawnames.split(';') #получаем список имен авторов
    lnames = [x.strip(' ') for x in lnames] #убираем лишние пробелы

    acount = len(lnames) #считаем число авторов
    df['author_count'][data.name]=acount #вносим число авторов в соотв. колонку 

    for x in lnames:   #цикл подсчета доли для каждого отдельного автора
            thisaffillist=[] #сюда складываем аффилиации данного автора
            a_affilcount=sum(x in y for y in laffils) #считаем число аффилиаций на автора
            for y in laffils: #составляем список всех аффилиаций данного автора
                if x in y:
                    thisaffillist.append(y)
            if any(x in str(thisaffillist) for x in match): #проверяем, если ли нужная аффилиация у данного автора
                counter = counter+(1/a_affilcount) #считаем долю за данного автора
    return counter/acount #подсчитываем и возвращаем долю

df['share'] = df.progress_apply(fracount, axis=1)
print ('saving to c:\Ivan\savedrecs.csv and c:\Ivan\savedrecs.xlsx...')
df.to_csv((r'c:\Ivan\savedrecs.csv'), sep='\t')
df.to_excel(r'c:\Ivan\savedrecs.xlsx')
print ('... done')  