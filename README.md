# WoS-Fractional-Counting-Script
Just a simple script to do fractional counting with Web of Science data

Это простой скрипт для долевого подсчета публикаций и цитирований организации в Web of Science. Он работает не с API, а с обычной выгрузкой из веб-интерфейса (нужный API WoS под названием Web Services Expanded стоит допольнительных существенных денег и не входит в нацподписку в РФ). 

Как считаем долю? Каждая публикация = 1 очко. Оно делится поровну между авторами. Доля организации от этого очка равна сумме долей аффилированных с ней авторов, а если у автора несколько аффилиаций, его очко делится поровну между ними. Пусть у статьи 3 автора: первый работает в Вышке, второй - в Гарварде, третий - в Вышке и МИАН. Доля каждого автора = 1\3. Доля организаций: Вышка = 1\3 (за первого автора) и 1\6 (за третьего, у него две аффилиации, поэтому дополнительно делим пополам) = 1\2, доля Гарварда = 1\3 (за второго автора), доля МИАН = 1\6 (за третьего автора).

**Алгоритм работы:**

1. Скачиваем из классического (не нового) интерфейса WoS нужные нам публикации порциями по 500 штук в варианте full record в формате other file formats - tab-delimited win utf-8 (другие кодировки тоже могут сработать). 
2. Если файлов несколько, склеиваем в один (например, в винде кладем все файлы в одну папку и запускаем в ней команду copy *.txt savedrecs.txt)
3. Убираем в текстовом редакторе последний (глючный) байт (в обычном notepad ставим курсор сразу после последнего символа в файле и усиленно жмем delete)
4. В скрипте правим **match** - список вариантов написания названия организации нужным образом. case-dependent! здесь нужно быть внимательными, чтобы не зацепить чужие аффилиации.
5. Запускаем код, при необходимости меняя адрес и название входного файла
6. Открываем результат, в последней строке доля, в предпоследней - число авторов. если доля = 0, смотрим колонку C1 (содержит аффилиации), выясняем, какое именно название не учлось, и добавляем его в список вариантов (шаг 4), затем снова запускаем код

Адрес для локального складирования данных можете поменять в самом конце скрипта. 

Скрипт не надо использовать для сдачи официальной отчетности. Никакой ответственности за корректность расчетов и тем более данных в первоисточнике я на себя не беру. Пользуйтесь на свой страх и риск. 

Любые доработки и замечания приветствуются, вносите через issues. Я не программист, знания python у меня начальные, не судите строго. 

Аналогичный скрипт для Scopus работает через API (входит в нацподписку) и попроще за счет наличия уникальных идентификаторов организаций: https://github.com/IvanSterligov/University-fractional-counting-with-Pybliometrics

Пополняемый открытый список вариантов названий вузов: https://openriro.github.io/ Вносите туда варианты названий своих вузов, будет здорово и всем полезно.
