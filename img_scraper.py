import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


def create_folder(folder_name):
    """Görsellerin kaydedileceği klasörü oluşturur."""
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)


def download_image(url, folder_name, num):
    """Görseli verilen URL'den indirir ve belirtilen klasöre kaydeder."""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            with open(os.path.join(folder_name, f"{num}.jpg"), "wb") as file:
                file.write(response.content)
            print(f"Downloaded Image {num}")
    except Exception as e:
        print(f"Failed to download Image {num}: {e}")


def scroll_to_bottom(driver):
    """Sayfanın tamamını aşağı kaydırarak tüm görselleri yükler."""
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)  # Görsellerin yüklenmesini bekle
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


def scrape_images(
    search_query,
    folder_name,
    driver_path,
    img_class,
    high_res_xpath,
    related_articles_class,
):
    """Google Görseller'den verilen arama sorgusu için görselleri indirir."""
    create_folder(folder_name)

    # ChromeDriver ayarları
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(driver_path), options=chrome_options)

    try:
        # Google Görseller'de arama yapma
        search_URL = f"https://www.google.com/search?q={search_query}&tbm=isch"
        driver.get(search_URL)
        time.sleep(2)

        # Sayfayı tamamen aşağı kaydırarak tüm görselleri yükle
        scroll_to_bottom(driver)

        # Görselleri toplama (Related Articles dışındaki görseller)
        image_elements = driver.find_elements(
            By.XPATH,
            f'//img[@class="{img_class}" and not(ancestor::div[contains(@class, "{related_articles_class}")])]',
        )
        print(f"Found {len(image_elements)} images.")

        # Görselleri tıklayarak büyük çözünürlükte indirme
        for idx, img_element in enumerate(image_elements):
            try:
                # Görsele tıkla
                driver.execute_script("arguments[0].click();", img_element)
                time.sleep(5)  # Tam boyutlu görselin yüklenmesini bekle

                # Tam çözünürlüklü görselin URL'sini al
                high_res_img = driver.find_element(By.XPATH, high_res_xpath)
                imageURL = high_res_img.get_attribute("src")

                if imageURL and imageURL.startswith("http"):
                    download_image(imageURL, folder_name, idx + 1)

            except Exception as e:
                print(f"Error with Image {idx + 1}: {e}")

    finally:
        driver.quit()
        print("All images downloaded.")


if __name__ == "__main__":
    QUERY = "red rainy day"
    FOLDER_NAME = "red_rainy_day"
    CHROME_DRIVER_PATH = (
        r"C:\Users\emrehan.gorgec\Desktop\Documents\Scripts\chromedriver.exe"
    )
    IMG_CLASS = "YQ4gaf"
    HIGH_RES_XPATH = (
        '//*[@id="Sva75c"]/div[2]/div[2]/div/div[2]/c-wiz/div/div[3]/div[1]/a/img[1]'
    )
    RELATED_ARTICLES_CLASS = "BA0zte"

    scrape_images(
        QUERY,
        FOLDER_NAME,
        CHROME_DRIVER_PATH,
        IMG_CLASS,
        HIGH_RES_XPATH,
        RELATED_ARTICLES_CLASS,
    )
