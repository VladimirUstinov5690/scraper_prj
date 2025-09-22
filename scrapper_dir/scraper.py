from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

url = 'https://www.coingecko.com/ru'

stop_scraping = False


def start_scraping() -> list[tuple[str, str, float, float, float]] | None:
    """Запускает скраппинг сайта криптовалют ->
    tuple(name, symbol, price, trading_volume, market_cap)"""
    global stop_scraping
    if stop_scraping:
        print('Сбор данных остановлен!')
        return
    
    opts = Options()
    opts.page_load_strategy = "none"
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                              options=opts)
    try:
        driver.get(url)
        # Ожидаем загрузку траницы
        WebDriverWait(driver, 20).until(
            expected_conditions.presence_of_element_located(
                (By.CSS_SELECTOR, "tbody tr")))
        print('Страница загружена!')
        
        row = driver.find_elements(By.CSS_SELECTOR, 'tbody tr')
        data_coins = []
        
        # Получаем имя, символ, стоимость, объем торгов, капитализацию криптовалюты
        for el in row:
            name = el.find_element(By.CSS_SELECTOR, 'div.tw-font-semibold')
            name_crypto = name.text.splitlines()[0].strip()
            symbol_crypto = name.text.splitlines()[1].strip()
            
            spans = el.find_elements(By.CSS_SELECTOR, 'span[data-price-usd]')
            if len(spans) < 3:
                continue
            price = round(float(spans[0].get_attribute("data-price-usd")), 2)
            trading_volume = round(
                float(spans[1].get_attribute("data-price-usd")), 2)
            market_cap = round(float(spans[2].get_attribute("data-price-usd")),
                               2)
            
            data_coins.append(
                (name_crypto, symbol_crypto, price, trading_volume,
                 market_cap))
        
        return data_coins
    
    except Exception as e:
        print("ОШИБКА:", e)
    finally:
        driver.quit()


def stop_scraper():
    """Установливает флаг для остановки скраппера."""
    global stop_scraping
    stop_scraping = True
