import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

folder_name = "sepetli_vinc"
if not os.path.exists(folder_name):
    os.makedirs(folder_name)


def download_image(url, folder_name, num):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            with open(os.path.join(folder_name, f"{num}.jpg"), "wb") as file:
                file.write(response.content)
            print(f"Downloaded Image {num}")
    except Exception as e:
        print(f"Failed to download Image {num}: {e}")


chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chromeDriverPath = r"C:\Users\emrehan.gorgec\Desktop\Documents\Scripts\chromedriver.exe"

driver = webdriver.Chrome(service=Service(chromeDriverPath), options=chrome_options)

# Google Görseller'de arama yapma
search_query = "sepetli vinç"
search_URL = f"https://www.google.com/search?q={search_query}&tbm=isch"
driver.get(search_URL)
time.sleep(2)

# Sayfayı tamamen aşağı kaydırarak tüm görselleri yükle
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)  # Görsellerin yüklenmesini bekle
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# Görselleri toplama (Related Articles dışındaki görseller)
image_elements = driver.find_elements(
    By.XPATH,
    '//img[@class="YQ4gaf" and not(ancestor::div[contains(@class, "BA0zte")])]',
)
print(f"Found {len(image_elements)} images.")

# Görselleri tıklayarak büyük çözünürlükte indirme
for idx, img_element in enumerate(image_elements):
    try:
        # Görsele tıkla
        driver.execute_script("arguments[0].click();", img_element)
        time.sleep(5)  # Tam boyutlu görselin yüklenmesini bekle

        # Tam çözünürlüklü görselin URL'sini al
        high_res_img = driver.find_element(
            By.XPATH,
            '//*[@id="Sva75c"]/div[2]/div[2]/div/div[2]/c-wiz/div/div[3]/div[1]/a/img[1]',
        )
        imageURL = high_res_img.get_attribute("src")

        # Görseli indir
        if imageURL and imageURL.startswith("http"):
            download_image(imageURL, folder_name, idx + 1)

    except Exception as e:
        print(f"Error with Image {idx + 1}: {e}")

# Tarayıcıyı kapat
driver.quit()
print("All images downloaded.")
