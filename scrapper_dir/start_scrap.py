import schedule
from scrapper_dir.scraper import start_scraping, stop_scraping
from scrapper_dir.db import add_to_db


def main():
    elements = start_scraping()
    if not elements:
        return schedule.CancelJob
    count_elements = add_to_db(elements)
    print(f'Добавлено {count_elements} записей!')
    return count_elements


def start_continuous_scraping():
    data = main()
    if isinstance(data, int) and not stop_scraping:
        schedule.every(1).minutes.do(main)
        while not stop_scraping and schedule.get_jobs():
            schedule.run_pending()
