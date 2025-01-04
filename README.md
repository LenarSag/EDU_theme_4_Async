# EDU_theme_2_parser

### Описание проекта
`EDU_theme_2_parser` — это парсер для автоматической загрузки бюллетеней по итогам торгов с сайта биржи [СПбМТСБ](https://spimex.com/markets/oil_products/trades/results/). Парсер извлекает необходимые данные из таблицы бюллетеня и сохраняет их в базу данных в таблицу `spimex_trading_results`.

---

## Функциональность парсера
Парсер выполняет следующие задачи:

1. Скачивает бюллетень по итогам торгов с указанного сайта.
2. Обрабатывает таблицу "Единица измерения: Метрическая тонна".
3. Фильтрует строки, где значение в столбце "Количество Договоров, шт." больше 0.
4. Извлекает следующие столбцы:
   - **Код Инструмента** (`exchange_product_id`)
   - **Наименование Инструмента** (`exchange_product_name`)
   - **Базис поставки** (`delivery_basis_name`)
   - **Объем Договоров в единицах измерения** (`volume`)
   - **Объем Договоров, руб.** (`total`)
   - **Количество Договоров, шт.** (`count`)
5. Сохраняет данные в таблицу `spimex_trading_results` с заданной структурой.

---

## Структура таблицы `spimex_trading_results`

| Поле               | Тип данных | Описание                                      |
|--------------------|------------|-----------------------------------------------|
| `id`               | SERIAL     | Первичный ключ                                |
| `exchange_product_id` | TEXT       | Код инструмента                               |
| `exchange_product_name` | TEXT     | Наименование инструмента                     |
| `oil_id`           | TEXT       | Первые 4 символа из `exchange_product_id`     |
| `delivery_basis_id` | TEXT       | Символы с 5 по 7 из `exchange_product_id`     |
| `delivery_basis_name` | TEXT     | Базис поставки                                |
| `delivery_type_id` | TEXT       | Последний символ из `exchange_product_id`     |
| `volume`           | NUMERIC    | Объем договоров в единицах измерения         |
| `total`            | NUMERIC    | Объем договоров в рублях                     |
| `count`            | INTEGER    | Количество договоров                         |
| `date`             | DATE       | Дата бюллетеня                                |
| `created_on`       | TIMESTAMP  | Дата и время создания записи                 |
| `updated_on`       | TIMESTAMP  | Дата и время обновления записи               |

---

## Логика обработки данных

Парсер обрабатывает код инструмента (`exchange_product_id`) и извлекает из него дополнительные поля:
- **oil_id** — первые 4 символа кода инструмента.
- **delivery_basis_id** — символы с 5 по 7 кода инструмента.
- **delivery_type_id** — последний символ кода инструмента.

---

## Пример работы парсера

### Исходные данные из бюллетеня:
| Код Инструмента | Наименование Инструмента | Базис поставки   | Объем Договоров в единицах измерения | Объем Договоров, руб. | Количество Договоров, шт. |
|-----------------|--------------------------|------------------|--------------------------------------|-----------------------|---------------------------|
| 1234AB1         | ДТ Евро-5                | Санкт-Петербург  | 500                                  | 25 000 000            | 5                         |
| 5678CD2         | Бензин АИ-92             | Москва           | 300                                  | 15 000 000            | 3                         |

### Результат в таблице `spimex_trading_results`:
| id  | exchange_product_id | exchange_product_name | oil_id | delivery_basis_id | delivery_basis_name | delivery_type_id | volume | total      | count | date       | created_on         | updated_on         |
|-----|---------------------|-----------------------|--------|------------------|---------------------|------------------|--------|------------|-------|------------|-------------------|-------------------|
| 1   | 1234AB1             | ДТ Евро-5             | 1234   | AB               | Санкт-Петербург     | 1                | 500    | 25000000.00 | 5     | 2025-01-04 | 2025-01-04 12:00  | 2025-01-04 12:00  |
| 2   | 5678CD2             | Бензин АИ-92          | 5678   | CD               | Москва              | 2                | 300    | 15000000.00 | 3     | 2025-01-04 | 2025-01-04 12:00  | 2025-01-04 12:00  |

---

## Инструкция по запуску

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/LenarSag/EDU_theme_2_parser
   cd EDU_theme_2_parser
   ```

2. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

3. Запустите парсер:
   ```bash
   python parser.py
   ```

---

## Требования к окружению
- Python 3.10+
- PostgreSQL
- Библиотеки: requests, pandas, sqlalchemy

