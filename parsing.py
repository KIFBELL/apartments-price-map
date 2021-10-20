from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import shutil


def create_empty_dir(dir_path):
    """creates empty dir to download offers in"""
    try:
        shutil.rmtree(dir_path)
    except:
        os.makedirs(dir_path, exist_ok=True)

def create_driver(city):
    """creates webdriver with disabled pic download and default dir to download files"""
    # pictures off
    chrome_options = webdriver.ChromeOptions()
    chrome_prefs = {}
    chrome_options.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}

    # download path
    destination = os.path.join(os.getcwd(), f"{city}_files")
    create_empty_dir(destination)

    chrome_prefs["download.default_directory"] = destination

    #     chrome_options.add_experimental_option('prefs', prefs)
    return webdriver.Chrome(os.path.join(os.getcwd(), 'chromedriver'), options=chrome_options)


def choose_appartment_layout(driver, cian_link):
    driver.get(cian_link)
    # open a combobox
    driver.find_elements_by_class_name("_025a50318d--button--2oXjq")[1].click()

    # rooms 3 4 5 6
    rooms = driver.find_elements_by_class_name('_025a50318d--button--39rK7')
    for room in rooms[2:]:
        room.click()
    # Studio apartment & free layout
    extended_rooms = driver.find_elements_by_class_name('_025a50318d--box--VTgYk')
    for room in extended_rooms:
        room.click()


def download_files(data, city):
    driver = create_driver(city)

    cian_link = 'https://www.cian.ru'
    cities = {"moscow": "Москва", "spb": "Санкт-Петербург", "ekaterinburg": "Екатерингбург"}
    for i, row in data.iterrows():
        choose_appartment_layout(driver, cian_link)

        search = driver.find_element_by_id("geo-suggest-input")
        if city == 'moscow':
            search.send_keys(f"{row.raion_name}, {row.okrug}, {cities[city]}")
        else:
            search.send_keys(f"{row.raion_name}, {cities[city]}")
        WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.CLASS_NAME, "_025a50318d--popper--c63zv")))
        search.send_keys(Keys.RETURN)
        driver.find_element_by_link_text('Найти').click()
        try:
            WebDriverWait(driver, 20).until(EC.url_contains("cat"))
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            driver.find_element_by_class_name("_93444fe79c--main--1-d6V").click()
        except:
            print(i, f"{row.raion_name}, {row.okrug}, Москва")


__all__ = ["download_files", "choose_appartment_layout", "create_empty_dir", "create_driver"]

if __name__ == "__main__":
    pass