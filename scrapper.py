import requests
from bs4 import BeautifulSoup
from time import sleep
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import ActionChains

def create_driver():

    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-notifications')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--shm-size=2g')
        options.add_argument('--no-sandbox')
        options.add_argument("--start-maximized")
        options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36")

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

# we retry for 3 times
for i in range(3):
    try:
        # go to the page
        driver = create_driver()
        url = 'http://www.szse.cn/application/search/index.html?keyword=%20签%20战略%20合作%20协议&r=1605350122601'
        driver.get(url)
        sleep(15)
        break
    except Exception as e:
        driver.quit()
        print(f"Fail to get the page. {e}")

# click buttons
try:
    btn = driver.find_element_by_xpath("//span[@class='text ellipsis' and contains(text(), '信息披露')]")
    ActionChains(driver).move_to_element(btn).double_click(btn).perform()
except Exception as e:
    print(f"Fail 1, {e}")
sleep(3)
try:
    btn = driver.find_element_by_xpath("//span[@class='text ellipsis' and contains(text(), '上市公司信息')]")
    ActionChains(driver).move_to_element(btn).double_click(btn).perform()
except Exception as e:
    print(f"Fail 2, {e}")
sleep(3)
try:
    btn = driver.find_element_by_xpath("//span[@class='text ellipsis' and contains(text(), '公告信息')]")
    ActionChains(driver).move_to_element(btn).click(btn).perform()
except Exception as e:
    print(f"Fail 3, {e}")

def save_pdf_urls(pdf_url):
    file_path = '/tmp/szes_pdfs'
    # if not os.path.exists(file_path):
    #     os.mkdir(file_path)
    with open(f"{file_path}.txt", "w") as file:
        file.write(pdf_url+"\n")

# get pdf urls of this page
def get_pdf_path(soup):
    try:
        items = soup.find("div", {"class":"article-search-result"}).find_all("div", {"class":"article-item index-length2"})
        for item in items[:2]:
            article_index = item.find('span', {"class":"artcile-index"}).text.strip()
            print(article_index)

            a = item.find('a', {"class":"text ellipsis pdf"}, href=True)
            pdf_url = a['href']
            title = a.text.strip()
            print(pdf_url)
            print(title)

            # TODO: we need the company code
            # https://stackoverflow.com/questions/48600143/find-number-after-a-substring-in-string/48600278
            company_code = item.find('p', {"class":"item-content ellipsis"}).text

            date = item.find('span', {"class":"pull-right"})
            print(date.text)
            print(f"Found: {pdf_url}")

    except Exception as e:
        print(f"Fail 5, can't get pdf url. {e}")
        return False
    return True

# go through each page for getting pdf urls
total_page = 2
bookmark_page = 0 # we need to reocrd which page we have been in case the process break up
for page in range(total_page):
    bookmark_page = page + 1
    print(f"===== {bookmark_page} =====")
    soup = BeautifulSoup(driver.page_source, "html.parser")
    done = get_pdf_path(soup)

    if done:
        try:
            print("XXX-1")
            btn = driver.find_element_by_xpath("//li[@class='next' and @data-show='next']//a")
            ActionChains(driver).move_to_element(btn).click(btn).perform()
            sleep(10)
            print("XXX-2")
        except Exception as e:
            print(f"Fail 4, can not move to next page. current page {bookmark_page}, {e}")
    else:
        print(f"Page {bookmark_page} is not completed.")
        break

# { 
#     "01":
#     {
#         "title": "company_code_2020-11-09_佳云科技：关于与原战略投资者签署战略合作协议之终止协议及认购协议之终止协议的公告",
#         "pdf": "http://disc.static.szse.cn/download/disc/disk02/finalpage/2020-11-09/c5ff1165-c0e2-4d53-b3cc-900b3b62b76e.PDF"
#     },
#     "02":
#     {
#         "title": "company_code_2020-11-09_佳云科技：关于与原战略投资者签署战略合作协议之终止协议及认购协议之终止协议的公告",
#         "pdf": "http://disc.static.szse.cn/download/disc/disk02/finalpage/2020-11-09/c5ff1165-c0e2-4d53-b3cc-900b3b62b76e.PDF"
#     },
# }

sleep(500)
driver.quit()
# 


# http://www.szse.cn/application/search/index.html?keyword=%20%E7%AD%BE%20%E6%88%98%E7%95%A5%20%E5%90%88%E4%BD%9C%20%E5%8D%8F%E8%AE%AE&r=1605350122601