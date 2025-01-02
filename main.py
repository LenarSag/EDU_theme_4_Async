import asyncio
from datetime import datetime
import os

from app.crud.trade_repository import add_trade_result, save_all
from app.db.database import async_session
from app.downloader.downloader import download_files
from app.downloader.files import find_xls_files
from app.parser.web_parser import scrape_reports
from app.parser.xls_parser import pandas_data_to_dict, parse_xls


BASE_URL = "https://spimex.com"
START_PAGE_URL = "/markets/oil_products/trades/results/"
TARGET_DATE = datetime(2024, 1, 1)
DOWNLOAD_FOLDER = "downloads"


async def main():
    # Шаг 1: Собираем ссылки на файлы
    download_links = await scrape_reports(BASE_URL, START_PAGE_URL, TARGET_DATE)

    # Шаг 2: Скачиваем файлы
    if download_links:
        await download_files(download_links, DOWNLOAD_FOLDER)
    else:
        print("Нет доступных файлов для скачивания.")

    # Шаг 3: Получаем список скачанных файлов
    downloaded_files = find_xls_files(DOWNLOAD_FOLDER)

    # Шаг 4: Парсим данные из файлов и сохраняем в бд
    for file in downloaded_files:
        trade_data = parse_xls(file)
        if trade_data is None or trade_data.empty:
            continue

        try:
            async with async_session() as session:
                for _, row in trade_data.iterrows():
                    trade_data = pandas_data_to_dict(row)
                    await add_trade_result(session, trade_data)

                await save_all(session)
        except Exception as e:
            print(f"Ошибка при сохранении данных из {file}: {e}")


if __name__ == "__main__":
    os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)
    asyncio.run(main())
