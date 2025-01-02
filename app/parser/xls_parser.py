import re

import pandas as pd
from numpy import nan


RELEVANT_COLUMNS = [
    "Код\nИнструмента",
    "Наименование\nИнструмента",
    "Базис\nпоставки",
    "Объем\nДоговоров\nв единицах\nизмерения",
    "Обьем\nДоговоров,\nруб.",
    "Количество\nДоговоров,\nшт.",
]
DATABASE_COLUMNS = {
    "Код\nИнструмента": "exchange_product_id",
    "Наименование\nИнструмента": "exchange_product_name",
    "Базис\nпоставки": "delivery_basis_name",
    "Объем\nДоговоров\nв единицах\nизмерения": "volume",
    "Обьем\nДоговоров,\nруб.": "total",
    "Количество\nДоговоров,\nшт.": "count",
}
TARGET_DATA_ROW = "Единица измерения: Метрическая тонна"
DATE_ROW = "Дата торгов:"
UNWANTED_PATTERN = ["Итого:", "Итого по секции:"]


def parse_trade_date(file_path: str) -> pd.Timestamp | None:
    """Извлекает из файла дату торгов."""

    # Загрузка файла эксель в Панду
    df_meta = pd.read_excel(file_path, header=None)
    # Поиск строки с данными по дате торгов
    date_row = df_meta[
        df_meta.apply(
            lambda row: row.astype(str).str.contains(DATE_ROW).any(),
            axis=1,
        )
    ].index

    if not date_row.empty:
        # Извлекаем дату (из второго столбца)
        date_str = str(df_meta.iloc[date_row[0], 1])

        # Ищем дату через re в формате "DD.MM.YYYY"
        date_match = re.search(r"\d{2}\.\d{2}\.\d{4}", date_str)
        if date_match:
            trade_date = pd.to_datetime(date_match.group(), format="%d.%m.%Y")
            return trade_date
        else:
            print(f"Дата торгов не найдена для: {file_path}")
            return None
    print(f"Строка с содержащая дату торгов не найденя для: {file_path}")
    return None


def parse_trade_data(file_path: str) -> pd.DataFrame | None:
    """Извлекает из файла данные торгов."""

    try:
        # Загрузка файла эксель в Панду
        df = pd.read_excel(file_path, header=None)

        # Поиск ряда откуда начинаются данные торгов
        start_row = df[
            df.apply(
                lambda row: row.astype(str).str.contains(TARGET_DATA_ROW).any(), axis=1
            )
        ].index
        if start_row.empty:
            print(f"Ключевая фраза/слово '{TARGET_DATA_ROW}' не найдено в файле.")
            return None

        # Извлечение данных по торгам
        start_row = start_row[0] + 1
        df = pd.read_excel(file_path, skiprows=start_row, header=0)

        # Определяем столбцы которые нас интересуют
        df = df[RELEVANT_COLUMNS]

        # Переименовываем столбцы
        df.rename(
            columns=DATABASE_COLUMNS,
            inplace=True,
        )

        # Добавляем столбцы на основе ранее полученных данных
        df["oil_id"] = df["exchange_product_id"].str[:4]
        df["delivery_basis_id"] = df["exchange_product_id"].str[4:7]
        df["delivery_type_id"] = df["exchange_product_id"].str[-1]

        # Удаляет пустые строки
        df.dropna(subset=["exchange_product_id", "exchange_product_name"], inplace=True)

        for col in ("volume", "total", "count"):
            # Переводит числовые данные в число
            df[col] = pd.to_numeric(df[col], errors="coerce")
            # Заменяет nan на None
            df[col] = df[col].replace(nan, None)

        return df

    except Exception as e:
        print(f"Ошибка обработки файла: {e}")
        return None


def remove_summary_rows(df: pd.DataFrame) -> pd.DataFrame:
    """Удаляет лишние строки."""

    df = df[
        ~df.apply(
            lambda row: row.astype(str).str.contains("|".join(UNWANTED_PATTERN)).any(),
            axis=1,
        )
    ]

    return df


def pandas_data_to_dict(row) -> dict:
    """Перводит данные из формата пандас в словарь."""

    return row.to_dict()


def parse_xls(file_path: str) -> pd.DataFrame | None:
    """Парсит файл xls."""

    trade_data = parse_trade_data(file_path)
    if trade_data is None or trade_data.empty:
        print(f"Не удалось найти данные торгов для {file_path}")
        return None

    trade_data = remove_summary_rows(trade_data)

    trade_date = parse_trade_date(file_path)
    if trade_date:
        trade_data["date"] = trade_date
    else:
        trade_data["date"] = None

    return trade_data
