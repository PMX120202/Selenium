from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# constants
START_ID = 'ctl00_ContentPlaceHolder1_ctl03_dpkTradeDate1_txtDatePicker'
END_ID =   'ctl00_ContentPlaceHolder1_ctl03_dpkTradeDate2_txtDatePicker'
BTN_ID = 'ctl00_ContentPlaceHolder1_ctl03_btSearch'
START_DATE = '1/7/2022'
END_DATE = '29/8/2022'

options = webdriver.ChromeOptions() 
options.add_experimental_option("excludeSwitches", ["enable-logging"])
# options.headless = True
# create a web driver
driver = webdriver.Chrome(options=options)

print('done setting up')

# tickers = ['VNI', 'VNM', 'FPT', 'HPG', 'POW', 'ACB']
unsuccess = []
tickers = ['VNM']

for ticker in tickers:
    content = []
    allow_write = True
    URL = f'https://s.cafef.vn/Lich-su-giao-dich-{ticker}-1.chn'
    filename = f'./myData/{ticker}.csv'
    
    # open the page
    driver.get(URL)
    
    # select the start + end dates
    start = driver.find_element(By.ID, START_ID)
    end = driver.find_element(By.ID, END_ID)
    btn = driver.find_element(By.ID, BTN_ID)
    
    start.send_keys(START_DATE)
    end.send_keys(END_DATE)
    btn.click()
    
    print(f'start scraping {ticker}')
    page = 1
    while True:
        try: 
            WebDriverWait(driver, 30).until(EC.staleness_of(driver.find_element(By.ID, 'GirdTable2')))
            table_tag = driver.find_element(By.ID, 'GirdTable2')
        except:
            print(f'No GirdTable2 in {ticker}')
            allow_write = False
            unsuccess.append(ticker)
            break
        try:
            print(f'scraping page {page}')
            
            tr_tags = table_tag.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')
            for tr_tag in tr_tags[2:3]:
                td_tags = tr_tag.find_elements(By.TAG_NAME, 'td')
                row = [td_tag.text for td_tag in td_tags]
                # print(row)
                # remove the unwanted elements
                row = row[:3] + row[5:-3] 
                print(row)
                
                # convert the string to float
                data = ','.join(row)
                
                # store data
                content.append(data)
        except:
            break
        
        # press the next button
        try:
            next_page_button = driver.find_element(By.CLASS_NAME, 'CafeF_Paging').find_element(By.LINK_TEXT, '>')
            next_page_button.click()
            # print(f'{ticker} swap page')
        except:
            break
        
        
        page += 1
        
    if not allow_write:
        continue
    print(f'done scraping {ticker} data >>>>>')
    with open(filename, 'w') as f:
        for line in content:
            f.write(line + '\n')