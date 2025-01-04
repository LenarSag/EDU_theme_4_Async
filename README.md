# EDU_theme_2_parser

Парсер, который скачивает бюллетень по итогам торгов с сайта биржи (https://spimex.com/markets/oil_products/trades/results/).

Достает из бюллетени необходимые столбцы (забрать только данные из таблицы «Единица измерения: Метрическая тонна», где по столбцу «Количество Договоров, шт.» значения больше 0):

a.  	Код Инструмента (exchange_product_id)
b.      Наименование Инструмента (exchange_product_name)
c.  	Базис поставки (delivery_basis_name)
d.      Объем Договоров в единицах измерения (volume)
e.      Объем Договоров, руб. (total)
f.       Количество Договоров, шт. (count)

Сохраняет полученные данные в таблицу «spimex_trading_results» со следующей структурой:

g.      id
h.      exchange_product_id
i.       exchange_product_name
j.       oil_id - exchange_product_id[:4]
k.  	delivery_basis_id - exchange_product_id[4:7]
l.       delivery_basis_name
m.	delivery_type_id - exchange_product_id[-1]
n.      volume
o.      total
p.      count
q.      date
r.       created_on
s.      updated_on


### Запуск проекта

Клонировать репозиторий и перейти в него в командной строке: 
```
https://github.com/LenarSag/EDU_theme_2_parser
```
Cоздать и активировать виртуальное окружение: 
```
python3.9 -m venv venv 
```
* Если у вас Linux/macOS 

    ```
    source venv/bin/activate
    ```
* Если у вас windows 
 
    ```
    source venv/Scripts/activate
    ```
```
python3.9 -m pip install --upgrade pip
```
Установить зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```

Запуск проекта:
```
python main.py
```