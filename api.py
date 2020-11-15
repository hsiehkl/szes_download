import requests, json, re, random, decimal
from io import StringIO
from html.parser import HTMLParser
from time import sleep

class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.text = StringIO()
    def handle_data(self, d):
        self.text.write(d)
    def get_data(self):
        return self.text.getvalue()

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def find_number(text):

    txt = ["证券代码：", "证券代码:", "股票代码：", "股票代码:", "证券代码： ", "股票代码： ", "证券号码：", "证券代号：", "证券代码 ：", "证券代码: "]

    n = ""

    for t in txt:
        try:
            n = re.findall(r'%s(\d+)' % t, text)[0]
            break
        except:
            pass

    if n == "":
        n = re.findall(r'\b(\d{6})\b', text)[0]  

    return n
    

def get_date(url):
    return url.rsplit("/", 2)[1]

def random_n(i):
    return decimal.Decimal(str(random.random()))

def save_pdf_urls(pdf_urls):
    with open(f"pdf_urls2.txt", "a") as file:
        for pdf_url in pdf_urls:
            file.write(str(pdf_url)+"\n")


total_page = 198
for i in range(total_page):
    page = i + 1
    sleep(1)
    print(f"Request page {page}...")

    successful = False
    retries = 3
    for _ in range(retries):
        try:
            url = f"http://www.szse.cn/api/search/content?random=0.36724872483259086"
            body = {"keyword": "签 战略 合作 协议",
                    "range": "title",
                    "currentPage": page,
                    "pageSize": 20,
                    "channelCode": "noticeInfo_hidden",
                    "orderby": "score"}
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'       
            }

            response = requests.request("POST", url, headers=headers, data = body, timeout=30)

            if response.status_code != 200:
                raise Exception("Bad response")

            successful = True
            break
        except Exception as e:
            print("*********************")
            print(f"Failed to request page {page}... {e}")
            print("*********************")
            sleep(5)
            pass

    if successful:
        print("Parsing data...")
        xl_data = []
        data = json.loads(response.text)["data"]
        for d in data:
            try:
                docpuburl = d["docpuburl"]
            except:
                print("XXX-1")
                docpuburl = ""
            
            try:
                code = find_number(d["doccontent"])
            except:
                print(d["doccontent"])
                print("XXX-3")
                code = ""
            
            try:
                doctitle = strip_tags(d["doctitle"])
            except:
                print("XXX-4")
                doctitle = ""

            try:
                date = get_date(docpuburl)
            except:
                print("XXX-5")
                date = ""
            
            title = "_".join([code, date, doctitle])
            print([title, docpuburl])
            xl_data.append([title, docpuburl])
        
        # write data into excel
        save_pdf_urls(xl_data)




