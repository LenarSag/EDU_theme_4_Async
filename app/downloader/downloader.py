import asyncio
from http import HTTPStatus
import re
import os

import aiohttp


async def download_file(
    session: aiohttp.ClientSession, url: str, download_folder: str
) -> None:
    """Скачивает файл по ссылке и сохраняет в папку."""

    try:
        async with session.get(url) as response:
            if response.status == HTTPStatus.OK:
                file_name = os.path.basename(url)
                date_match = re.search(r"\d{8}", file_name)
                if date_match:
                    date_str = date_match.group(
                        0
                    )  # Извлекаем дату в формате "YYYYMMDD"
                    file_name = f"{date_str}.xls"
                else:
                    print(
                        f"Дата не найдена в имени файла {file_name}. Используется имя по умолчанию."
                    )
                    file_name = "default.xls"
                file_path = os.path.join(download_folder, file_name)

                with open(file_path, "wb") as file:
                    file.write(await response.read())
                print(f"Файл {file_name} загружен.")
            else:
                print(f"Ошибка загрузки файла {url}: {response.status}")
    except Exception as e:
        print(f"Ошибка при скачивании {url}: {e}")


async def download_files(download_links: list[str], download_folder: str) -> None:
    """Асинхронно скачивает все файлы по ссылкам."""

    async with aiohttp.ClientSession() as session:
        await asyncio.gather(
            *[download_file(session, link, download_folder) for link in download_links]
        )
