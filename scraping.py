import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd 

def get_page_urls(page_number):
    page_url = f"https://www.mydealz.de/new?page={page_number}"
    product_urls = []
    
    driver.get(page_url)
    driver.implicitly_wait(10)  
    time.sleep(2) 

    try:
            modal_close_xpath = '//*[@id="main"]/div[3]/div[3]/div[4]/div[2]/div/section/div/div/div/div/div/div[2]/div[2]/button[1]'
            modal_close = driver.find_element(By.XPATH, modal_close_xpath)
            modal_close.click()
            print("modal clicked")
    except:
            print("no modal")
    time.sleep(3)

    
    container_elements = driver.find_elements(By.CSS_SELECTOR, ".cept-tt.thread-link.linkPlain.thread-title--list.js-thread-title")
    for element in container_elements:
        link = element.get_attribute('href')
        product_urls.append(link)
    
    return product_urls

def get_content(page_url):
    driver.get(page_url)
    driver.implicitly_wait(10)  
    time.sleep(2)


    product_dict = dict()
    product_dict["url"] = page_url
    try:
        title = driver.find_element(By.CSS_SELECTOR,".text--b.size--all-xl.size--fromW3-xxl").text
        product_dict["title"] = title
    except:
        product_dict["title"] = ""

    try:
        description = driver.find_element(By.CSS_SELECTOR,".userHtml.userHtml-content.overflow--wrap-break.space--mt-3").text
        product_dict["description"] = description
    except:
        product_dict["description"] = ""


    try:
        price = driver.find_element(By.CSS_SELECTOR,".threadItemCard-price.text--b.thread-price").text
        product_dict["price"] = price
    except:
        product_dict["price"] = ""

    return product_dict
if __name__ == "__main__":
      
    options = Options()
    options.add_argument('--start-maximized')
    

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    number_of_pages = 1
    all_product_urls = list()

    for page in range(1, number_of_pages + 1):
        urls = get_page_urls(page)
        all_product_urls.extend(urls)
        print(f"Page {page} done")

    data_list = list()

    for url in all_product_urls[:3]:
        current_dict = get_content(url)
        data_list.append(current_dict)

    df = pd.DataFrame(data_list)
    df.to_csv("data.csv",index=False)


    driver.quit()



