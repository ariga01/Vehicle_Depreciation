import time
import pandas as pd
import numpy as np
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Driver Section
options = Options()
options.binary_location = r'C:\Program Files\Google\Chrome Beta\Application\chrome.exe'
prefs = {"enable_do_not_track": True}
options.add_experimental_option("prefs", prefs)
chrome = Service("chromedriver.exe")
driver = webdriver.Chrome(options=options, service=chrome)
driver.set_window_size(1024, 600)
driver.maximize_window()


# Function
def get_attribute_css(tag):
    try:
        att = driver.find_element(By.CSS_SELECTOR, tag).get_attribute("innerHTML")
    except:
        att = np.NaN

    return att

def get_attribute_xpath(tag):
    try:
        att = driver.find_element(By.XPATH, tag).get_attribute("innerHTML")
    except:
        att = np.NaN

    return att

def get_attribute_class(tag):
    try:
        attribute_data = driver.find_element(By.CLASS_NAME, tag)
        att = BeautifulSoup(attribute_data.get_attribute('outerHTML'), 'html.parser').text
    except:
        att = np.NaN
    return att


area_list = ['jakarta-dki_g2000007','jawa-barat_g2000009','jawa-timur_g2000011','banten_g2000004','jawa-tengah_g2000010','yogyakarta-di_g2000032']
car_list = ['avanza', 'xpander', 'brio', 'rush', 'innova','cr-v', 'hr-v', 'jazz', 'yaris']
bike_list = ['beat','vario-125','scoopy','vario-150','mio']
brand_dict = dict({
    'toyota avanza' : 'toyota',
    'toyota rush' : 'toyota',
    'toyota innova' : 'toyota',
    'toyota yaris' : 'toyota',
    'mitsubishi xpander' : 'mitsubishi',
    'honda brio' : 'honda',
    'honda crv' : 'honda',
    'honda hrv' : 'honda',
    'honda jazz' : 'honda',
    'beat' : 'honda',
    'vario-125' : 'honda',
    'scoopy' : 'honda',
    'vario-150' : 'honda',
    'mio' : 'yamaha'
})


# Call value using key
def get_value(key_value):
    for key, value in brand_dict.items():
        if key_value == key:
            return value

    return "key doesn't exist"


attribute = []


# Main loop for car
for area in area_list:
    for car in car_list:
        for i in range(1, 101):
            try:
                link = f'https://www.olx.co.id/{area}/mobil_c86/q-{car}?page={i}&filter=price_min_30000000'
                driver.get(link)
                time.sleep(3)
            except:
                pass

            try:
                lists = driver.find_element(By.CLASS_NAME, 'rl3f9._3mXOU')
                card = lists.find_elements(By.CLASS_NAME, 'EIR5N')
            except:
                break

            full_list = []

            for item in card:
                link = item.find_element(By.TAG_NAME, 'a').get_attribute('href')
                full_list.append(link)

            for webpage in full_list:
                try:
                    driver.get(webpage)
                except:
                    pass
                time.sleep(2.5)

                title = get_attribute_class("_35xN1")
                price = get_attribute_class("_3FkyT")
                brand = get_value(car)
                milage = get_attribute_xpath('//*[@id="container"]/main/div/div/div/div[5]/div[1]/div[1]/div/div/div[4]/div[2]/div')
                loc = get_attribute_xpath('//*[@id="container"]/main/div/div/div/div[5]/div[2]/div[2]/div[3]/div[1]/div[2]/div')
                trans = get_attribute_xpath('//*[@id="container"]/main/div/div/div/div[5]/div[1]/div[1]/div/div/div[4]/div[3]/div')
                fuel = get_attribute_xpath('//*[@id="container"]/main/div/div/div/div[5]/div[1]/div[1]/div/div/div[4]/div[1]/div')

                if pd.isna(title) == False:
                    title_s = re.sub(r'[^a-zA-Z ]+', '', title).strip()
                    if title_s == 'honda brio satya':
                        title_s = 'honda brio'
                    elif title_s == 'toyota kijang innova':
                        title_s = 'toyota innova'
                    try:
                        brand_n = brand_dict[title_s]
                    except KeyError:
                        brand_n = np.NaN
                    years = int(re.findall("\d+", title)[0])
                else:
                    title_s = np.NaN
                    brand_n = np.NaN
                    years = np.NaN
                if pd.isna(price) == False:
                    price = int(''.join(re.findall("\d+", price)))
                else:
                    price = np.NaN


                to_list = {
                    'title': title_s,
                    'price': price,
                    'brand': brand_n,
                    'type': car,
                    'years': years,
                    'milage': milage,
                    'location': loc,
                    'vehicle_type' : 'car',
                    'url': webpage,
                    'transmission': trans,
                    'fuel' : fuel
                }
                print(to_list, 'page :', i)
                attribute.append(to_list)

attribute = pd.DataFrame(data=attribute)
attribute.to_csv('Output\Early_Car_Scraped.csv', index=False)



attribute = []


# Main loop for bike
for area in area_list:
    for bike in bike_list:
        for i in range(1, 101):
            try:
                link = f'https://www.olx.co.id/{area}/motor_c87/q-{bike}?page={i}&filter=price_min_1000000'
                driver.get(link)
                time.sleep(3)
            except:
                pass

            try:
                lists = driver.find_element(By.CLASS_NAME, 'rl3f9._3mXOU')
                card = lists.find_elements(By.CLASS_NAME, 'EIR5N')
            except:
                break

            full_list = []

            for item in card:
                link = item.find_element(By.TAG_NAME, 'a').get_attribute('href')
                full_list.append(link)

            for webpage in full_list:
                try:
                    driver.get(webpage)
                except:
                    pass

                time.sleep(2.5)

                title = get_attribute_css("span[data-aut-id='itemTitle']")
                price = get_attribute_css("span[data-aut-id='itemPrice']")
                brand = get_value(bike)
                years = get_attribute_css("span[data-aut-id='value_m_year']")
                type = bike
                milage = get_attribute_css("span[data-aut-id='value_mileage']")
                loc = get_attribute_xpath('//*[@id="container"]/main/div/div/div/div[5]/div[1]/div/section/div/div[1]/div/span')

                if pd.isna(years) == False:
                    years = int(years)
                else:
                    years = np.NaN
                if pd.isna(price) == False:
                    price = int(''.join(re.findall("\d+", price)))
                else:
                    price = np.NaN

                to_list = {
                'title': title,
                'price': price,
                'brand' : brand,
                'type' : bike,
                'years': years,
                'type' : type,
                'milage': milage,
                'location': loc,
                'vehicle_type' : 'bike',
                'url' : webpage
                }
                print(to_list, 'page :', i)
                attribute.append(to_list)

attribute = pd.DataFrame(data=attribute)
attribute.to_csv('Output\Early_Bike_Scraped.csv', index=False)