import schedule
from scraper import start_scraping, stop_scraping
from db import add_to_db


def main():
    elements = start_scraping()
    if not elements:
        return schedule.CancelJob
    count_elements = add_to_db(elements)
    print(f'Добавлено {count_elements} записей!')
    return count_elements


if __name__ == '__main__':
    data = main()
    if isinstance(data, int) and not stop_scraping:
        schedule.every(1).minutes.do(main)
        while not stop_scraping and schedule.get_jobs():
            schedule.run_pending()
