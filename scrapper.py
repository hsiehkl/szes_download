import requests
from bs4 import BeautifulSoup
# import pandas as pd
# import datetime
# from concurrent.futures import ProcessPoolExecutor, as_completed
# import time
from time import sleep

# base_url = 'http://www.szse.cn/application/search/index.html?keyword=%20签%20战略%20合作%20协议&r=1605350122601'
# headers = {
#     'user-agent': 
#     'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'
#     }

# url = base_url
# response = requests.get(url=url, headers=self.headers)
# sleep(5)
# soup = BeautifulSoup(response.content, 'html.parser')
    
# element = soup.find('li', attrs={'data-id': 'disclosure', 'data-level': '2'})



from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
# from utils import print, check_clicks, get_cookies_dir, get_url, cleanup_cookies
from selenium.webdriver import ActionChains
# import os, json,

def create_driver():

    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-notifications')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--shm-size=2g')
        options.add_argument('--no-sandbox')
        options.add_argument("--start-maximized")
        options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36")

        # Get rid of save password dialog
        # options.add_experimental_option('prefs', {
        #     'credentials_enable_service': False,
        #     'profile': {
        #         'password_manager_enabled': False
        #     }
        # })

        while True:
            print('Trying to obtain the driver')
            try:
                print('Installing driver')
                driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
                print('Successfully installed driver')
            except:
                print('Exception... Now searching for it in "./chromedriver"')
                driver = webdriver.Chrome(executable_path="./chromedriver", options=options)
            print("Waiting 7 seconds")
            driver.implicitly_wait(7)
            break
        print('Return Driver')

    except Exception as e:
        print(f'We can not create a driver.', e)
        return None

    driver.set_page_load_timeout(120)
    return driver

from selenium.webdriver import ActionChains

driver = create_driver()
url = 'http://www.szse.cn/application/search/index.html?keyword=%20签%20战略%20合作%20协议&r=1605350122601'
driver.get(url)
sleep(15)

try:
    btn = driver.find_element_by_xpath("//span[@class='text ellipsis' and contains(text(), '信息披露')]")
    ActionChains(driver).move_to_element(btn).double_click(btn).perform()
except:
    print("Fail 1")
sleep(5)
try:
    btn = driver.find_element_by_xpath("//span[@class='text ellipsis' and contains(text(), '上市公司信息')]")
    ActionChains(driver).move_to_element(btn).double_click(btn).perform()
except:
    print("Fail 2")
sleep(5)
try:
    btn = driver.find_element_by_xpath("//span[@class='text ellipsis' and contains(text(), '公告信息')]")
    ActionChains(driver).move_to_element(btn).click(btn).perform()
except:
    print("Fail 3")

soup = BeautifulSoup(driver.page_source, "html.parser")
items = soup.find("div", {"class":"article-search-result"}).find_all("div", {"class":"article-item index-length2"})

for item in items[:3]:
    a = item.find('a', {"class":"text ellipsis pdf"}, href=True)
    print("Found the URL:", a['href'])

sleep(500)
driver.quit()
# 


# http://www.szse.cn/application/search/index.html?keyword=%20%E7%AD%BE%20%E6%88%98%E7%95%A5%20%E5%90%88%E4%BD%9C%20%E5%8D%8F%E8%AE%AE&r=1605350122601