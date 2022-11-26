from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

tickers = ['VNM', 'FPT', 'VNI', 'HPG', 'POW', 'ACB']
START_DATE = '1/7/2022'
END_DATE = '29/8/2022'
START_BTN_ID = 'ctl00_ContentPlaceHolder1_ctl03_dpkTradeDate1_txtDatePicker'
END_BTN_ID = 'ctl00_ContentPlaceHolder1_ctl03_dpkTradeDate2_txtDatePicker'
WATCH_BTN_ID = 'ctl00_ContentPlaceHolder1_ctl03_btSearch'

options = webdriver.ChromeOptions() 
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(options=options)


for ticker in tickers:
    URL = f'https://s.cafef.vn/Lich-su-giao-dich-{ticker}-1.chn'

    driver.get(URL)

    start = driver.find_element(By.ID, START_BTN_ID)
    end = driver.find_element(By.ID, END_BTN_ID)
    btn = driver.find_element(By.ID, WATCH_BTN_ID)

    start.send_keys(START_DATE)
    end.send_keys(END_DATE)
    btn.click()


    content = []
    while True:
        WebDriverWait(driver, 30).until(EC.staleness_of(driver.find_element(By.ID, 'GirdTable2')))
        table = driver.find_element(By.ID, 'GirdTable2')
        
        tr_tags = table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')
        td_tags = tr_tags[0].find_elements(By.TAG_NAME, 'td')
        for td_tag in td_tags:
            print(td_tag.text)    
    


