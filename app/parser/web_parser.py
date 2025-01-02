from datetime import datetime
from http import HTTPStatus
from typing import Optional

import aiohttp
from bs4 import BeautifulSoup


async def fetch_page(session: aiohttp.ClientSession, url: str) -> str:
    """Загружает содержимое страницы."""

    async with session.get(url) as response:
        if response.status != HTTPStatus.OK:
            print(f"Ошибка загрузки страницы {url}: {response.status}")
            return ""
        return await response.text()


def get_daily_trade_blocks(html: str) -> Optional[list]:
    """Ищет все блоки дневных торгов на странице."""

    soup = BeautifulSoup(html, "html.parser")
    daily_accordeon = soup.find("div", class_="accordeon-inner")
    if daily_accordeon:
        return daily_accordeon.find_all("div", class_="accordeon-inner__wrap-item")
    return None


def exctract_and_check_date(blocks, target_date):
    """Проверяет блоки на целевую дату."""

    checked_links = []
    stop_scraping = False

    for block in blocks:
        date_paragraph = block.find("p")
        if date_paragraph:
            date_text = date_paragraph.find("span").text.strip()
            trade_date = datetime.strptime(date_text, "%d.%m.%Y")

            # Если дата меньше целевой, остановить обработку
            if trade_date < target_date:
                stop_scraping = True
                break
            checked_links.append(block)

    return checked_links, stop_scraping


def exctract_download_links(base_url: str, blocks: list) -> list[str]:
    """Извлекает ссылки на файлы."""

    download_links = []
    for block in blocks:
        # Ищем ссылки на файлы
        link_tag = block.find("a", class_="accordeon-inner__item-title link xls")
        if link_tag and link_tag.get("href"):
            download_links.append(base_url + link_tag.get("href"))

    return download_links


def get_next_page_url(html: str):
    """Возвращает ссылку на следующую страницу."""

    soup = BeautifulSoup(html, "html.parser")

    pagination_container = soup.find("div", class_="bx-pagination-container")
    if not pagination_container:
        return None

    next_page_li = pagination_container.find("li", class_="bx-pag-next")
    if next_page_li:
        next_page_link = next_page_li.find("a", href=True)
        if next_page_link:
            return next_page_link.get("href")

    return None


async def scrape_reports(
    base_url: str, start_page_url: str, target_date: datetime
) -> list[str]:
    """Основная функция для сбора ссылок с учетом даты."""

    async with aiohttp.ClientSession() as session:
        current_page_url = base_url + start_page_url
        all_download_links = []

        while current_page_url:
            # Загружаем страницу
            page_html = await fetch_page(session, current_page_url)
            if not page_html:
                break

            # Извлекаем блоки дневых торгов
            trade_blocks = get_daily_trade_blocks(page_html)
            if trade_blocks:
                # Проверяем дату
                checked_blocks, stop_scraping = exctract_and_check_date(
                    trade_blocks, target_date
                )

                # Получаем ссылки
                download_link = exctract_download_links(base_url, checked_blocks)
                all_download_links.extend(download_link)

                # Прекращаем извлечение страниц если достигли целевой даты
                if stop_scraping:
                    break

                # Получаем URL следующей страницы
                next_page_url = get_next_page_url(page_html)
                if next_page_url:
                    current_page_url = base_url + next_page_url
                    print(current_page_url)
                else:
                    break

        return all_download_links
