# 地址轉換成經緯度
import csv
import time
import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def crawler(loc):

        url = 'https://tools.wingzero.tw/archive/get-geometry/tw'
        driver = webdriver.Chrome('./crawler_drive/chromedriver')
        driver.get(url)

        input_form = driver.find_element_by_id("address")
        input_form.send_keys(loc)
        btn = driver.find_element_by_id("getGeo").click()
        time.sleep(1)
        lng = driver.find_element_by_id("lng").get_attribute('value')
        lat = driver.find_element_by_id("lat").get_attribute('value')

        print([loc, lng, lat])
        save_to_csv([loc, lng, lat])
        driver.close()

def save_to_csv(input_list):
    with open("./data/new_residential_burglary.csv", "a") as fp:
        wr = csv.writer(fp, dialect='excel')
        wr.writerow(input_list)

if __name__ == '__main__':
    pd.options.mode.chained_assignment = None
    # import data
    residential_data_path = './data/10401_10811_residential_burglary.csv'
    residential_data = pd.read_csv(residential_data_path, engine='python')
    residential_data = residential_data.rename(columns={'編號': 'No', '發生(現)日期': 'date', '案類': 'type',\
                                                    '發生時段': 'time', '發生(現)地點': 'location'})
    residential_data['city'] = residential_data.location.str[:3]
    residential_data['area'] = residential_data.location.str[3:6]

    filtered_data = residential_data[(residential_data.city == '台北市')]

    for i, loc in enumerate(filtered_data.location):
        print(i)
        crawler(loc)
