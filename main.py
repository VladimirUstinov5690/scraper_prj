from scraper import start_scraping
from db import write_to_db


def main():
    elements = start_scraping()
    count_elements = write_to_db(elements)
    print(f'Добавлено {count_elements} записей!')


if __name__ == '__main__':
    main()
