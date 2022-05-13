from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
import time

coin_count = 20


def getContent():
    options = Options()
    caps = DesiredCapabilities().CHROME
    caps['pageLoadStrategy'] = 'eager'

    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument('--headless')
    options.add_argument('--log-level=3')
    options.add_argument('--window-size=1300x1000')
    options.add_argument('--mute-audio')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-gpu')

    #userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.56 Safari/537.36'
    # options.add_argument(f'user-agent={userAgent}')

    driver = webdriver.Chrome(
        desired_capabilities=caps, options=options)

    driver.get('https://coinmarketcap.com')
    try:
        for i in range(0, coin_count):
            driver.execute_script(
                f'window.scrollTo({i*100}, {(i+1)*100});')
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f'/html/body/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[5]/table/tbody/tr[{i+1}]/td[3]/div/a/div/div/p')))
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f'/html/body/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[5]/table/tbody/tr[{i+1}]/td[4]/div/a/span')))
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f'/html/body/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[5]/table/tbody/tr[{i+1}]/td[7]/p/span[2]')))
    finally:
        time.sleep(1)
        content = driver.page_source
        driver.close()
        return content


def parseContent(content):
    data = []
    dataIndex = []

    soup = bs(content, 'lxml')
    table = soup.find(name='table', class_='h7vnx2-2 czTsgW cmc-table')

    tbody = table.find('tbody')
    rows = tbody.find_all('tr', limit=coin_count)

    for row in rows:
        try:
            cols = row.find_all('td', limit=7)

            parent_element = cols[2].find(
                name='div', class_='sc-16r8icm-0 escjiH')
            name = \
                parent_element.find(
                    name='p', class_='sc-1eb5slv-0 iworPT').text
            short_name = \
                parent_element.find(
                    name='p', class_='sc-1eb5slv-0 gGIpIK coin-item-symbol').text

            parent_element = cols[6].find(
                name='p', class_='sc-1eb5slv-0 hykWbK')
            market_cap = \
                parent_element.find(
                    name='span', class_='sc-1ow4cwt-1 ieFnWP').text

            parent_element = cols[3].find(
                name='div', class_='sc-131di3y-0 cLgOOr')
            price = parent_element.find(name='a', class_='cmc-link').text
            data.append([name, short_name, market_cap, price])
        except:
            continue

    for i in range(len(data)):
        dataIndex.append([i, data[i][0]])

    dataIndex.sort(key=lambda x: x[1])
    yield data
    yield dataIndex


def drawUpHorizLine():
    print('\u250C', end='')
    for i in range(0, 5):
        print('\u2500', end='')
    print('\u252C', end='')
    for i in range(0, 25):
        print('\u2500', end='')
    print('\u252C', end='')
    for i in range(0, 10):
        print('\u2500', end='')
    print('\u252C', end='')
    for i in range(0, 20):
        print('\u2500', end='')
    print('\u252C', end='')
    for i in range(0, 20):
        print('\u2500', end='')
    print('\u2510')
    print('\u2502%5s\u2502%25s\u2502%10s\u2502%20s\u2502%20s\u2502' %
          ('Index', 'Full name', 'Short Name', 'Market Cap', 'Price'))
    drawMidHorizLine()


def drawMidHorizLine():
    print('\u251C', end='')
    for i in range(0, 5):
        print('\u2500', end='')
    print('\u253C', end='')
    for i in range(0, 25):
        print('\u2500', end='')
    print('\u253C', end='')
    for i in range(0, 10):
        print('\u2500', end='')
    print('\u253C', end='')
    for i in range(0, 20):
        print('\u2500', end='')
    print('\u253C', end='')
    for i in range(0, 20):
        print('\u2500', end='')
    print('\u2524')


def drawLowHorizLine():
    print('\u2514', end='')
    for i in range(0, 5):
        print('\u2500', end='')
    print('\u2534', end='')
    for i in range(0, 25):
        print('\u2500', end='')
    print('\u2534', end='')
    for i in range(0, 10):
        print('\u2500', end='')
    print('\u2534', end='')
    for i in range(0, 20):
        print('\u2500', end='')
    print('\u2534', end='')
    for i in range(0, 20):
        print('\u2500', end='')
    print('\u2518')


def printData(data):
    drawUpHorizLine()
    for idx, i in enumerate(data):
        print('\u2502%5d\u2502%25s\u2502%10s\u2502%20s\u2502%20s\u2502' %
              (idx+1, i[0], i[1], i[2], i[3]))
        if idx != len(data)-1:
            drawMidHorizLine()
    drawLowHorizLine()


def binarySearch(data, need):
    cur = 0
    l = 0
    r = len(data)-1
    while(l < r):
        cur = int((l+r)/2)
        if (data[cur][1] < need):
            l = cur+1
        else:
            r = cur
    if (data[r][1] == need):
        return data[r][0]
    else:
        return -1


def printFound(data, index):
    drawUpHorizLine()
    print('\u2502%5d\u2502%25s\u2502%10s\u2502%20s\u2502%20s\u2502' %
          (index+1, data[index][0], data[index][1], data[index][2], data[index][3]))
    drawLowHorizLine()


data = []
dataIndex = []

try:
    coin_count = int(input('Write the cryptocurrency count needed: '))
except:
    print('Wrong input type')
    sys.exit()

if coin_count < 1 or coin_count > 100:
    print('Count may be only a number between 1 and 100')
    sys.exit()

content = getContent()
data, dataIndex = parseContent(content)

printData(data)

need = ''
index = -1
while (True):
    need = input(
        'Write the name of the required cryptocurrency or 0 to cancel:')
    if (need == '0'):
        break
    index = binarySearch(dataIndex, need)
    if (index == -1):
        print('Not found.')
    else:
        printFound(data, index)
