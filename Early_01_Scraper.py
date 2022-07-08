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
def get_values(css_tag="BLANK", class_tag="BLANK", xpath_tag="BLANK"):
    css_s = bool(css_tag)
    class_s = bool(class_tag)
    xpath_s = bool(xpath_tag)

    att = np.NaN

    if css_s != "BLANK":
        try:
            att = driver.find_element(By.CSS_SELECTOR, css_tag).get_attribute("innerHTML")
        except:
            att = np.NaN

    if pd.isna(att) == True and class_s != "BLANK":
        try:
            attribute_data = driver.find_element(By.CLASS_NAME, class_tag)
            att = BeautifulSoup(attribute_data.get_attribute('outerHTML'), 'html.parser').text
        except:
            att = np.NaN

    if pd.isna(att) == True and xpath_s != "BLANK":
        try:
            att = driver.find_element(By.XPATH, xpath_tag).get_attribute("innerHTML")
        except:
            att = np.NaN

    return att


area_list = ['jakarta-dki_g2000007','jawa-barat_g2000009','jawa-timur_g2000011','banten_g2000004','jawa-tengah_g2000010','yogyakarta-di_g2000032']
car_list = ['avanza', 'xpander', 'brio', 'rush', 'innova','cr-v', 'hr-v', 'jazz', 'yaris']
bike_list = ['beat','vario-125','scoopy','vario-150','mio']
brand_dict = {
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
}
type_dict = {
    'toyota avanza' : 'avanza',
    'toyota rush' : 'rush',
    'toyota innova' : 'innova',
    'toyota yaris' : 'yaris',
    'mitsubishi xpander' : 'xpander',
    'honda brio' : 'brio',
    'honda crv' : 'cr-v',
    'honda hrv' : 'hr-v',
    'honda jazz' : 'jazz'
}

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

                title = get_values(
                    css_tag = "span[data-aut-id='itemTitle']",
                    class_tag = "_35xN1",
                    xpath_tag ='//*[@id="container"]/main/div/div/div/div[5]/div[1]/div[1]/div[1]/div/div[2]'
                )
                price = get_values(
                    css_tag = "span[data-aut-id='itemTitle']",
                    class_tag = "span[data-aut-id='itemPrice']",
                    xpath_tag ='//*[@id="container"]/main/div/div/div/div[5]/div[2]/div[1]/div/div[1]'
                )
                brand = get_value(car)
                milage = get_values(
                    xpath_tag ='//*[@id="container"]/main/div/div/div/div[5]/div[1]/div[1]/div/div/div[4]/div[2]/div'
                )
                loc = get_values(
                    xpath_tag ='//*[@id="container"]/main/div/div/div/div[5]/div[2]/div[2]/div[3]/div[1]/div[2]/div'
                )
                trans = get_values(
                    xpath_tag ='//*[@id="container"]/main/div/div/div/div[5]/div[1]/div[1]/div[1]/div/div[4]/div[3]/div'
                )
                fuel = get_values(
                    xpath_tag ='//*[@id="container"]/main/div/div/div/div[5]/div[1]/div[1]/div[1]/div/div[4]/div[1]/div'
                )

                if pd.isna(title) == False:
                    title_s = re.sub(r'[^a-zA-Z ]+', '', title).strip()
                    if title_s == 'honda brio satya':
                        title_s = 'honda brio'
                    elif title_s == 'toyota kijang innova':
                        title_s = 'toyota innova'
                    elif title_s == 'toyota kijang':
                        title_s = 'toyota innova'
                    try:
                        brand_n = brand_dict[title_s]
                    except KeyError:
                        brand_n = np.NaN
                    try:
                        types = type_dict[title_s]
                    except KeyError:
                        types = np.NaN
                    years = int(re.findall("\d+", title)[0])
                else:
                    title_s = np.NaN
                    brand_n = np.NaN
                    years = np.NaN
                    types = np.NaN
                if pd.isna(price) == False:
                    price = int(''.join(re.findall("\d+", price)))
                else:
                    price = np.NaN
                if pd.isna(milage) == False:
                    try:
                        milage_s = re.sub(r'.Km|.km', '', milage)
                    except:
                        milage_s = milage

                to_list = {
                    'title': title_s,
                    'price': price,
                    'brand': brand_n,
                    'type': types,
                    'years': years,
                    'milage': milage_s,
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

                title = get_values(
                    css_tag="span[data-aut-id='itemTitle']",
                    xpath_tag='//*[@id="container"]/main/div/div/div/div[5]/div[1]/div/section/h1'
                )
                price = get_values(
                    css_tag="span[data-aut-id='itemPrice']",
                    xpath_tag='//*[@id="container"]/main/div/div/div/div[5]/div[1]/div/section/span[1]'
                )
                brand = get_value(bike)
                years = get_values(
                    css_tag="span[data-aut-id='value_m_year']",
                    xpath_tag='//*[@id="container"]/main/div/div/div/div[4]/section[1]/div/div/div[1]/div/div[3]/div/span[2]'
                )
                milage = get_values(
                    css_tag="span[data-aut-id='value_mileage']",
                    xpath_tag='//*[@id="container"]/main/div/div/div/div[4]/section[1]/div/div/div[1]/div/div[4]/div/span[2]'
                )
                loc = get_values(
                    xpath_tag='//*[@id="container"]/main/div/div/div/div[5]/div[1]/div/section/div/div[1]/div/span'
                )

                if pd.isna(years) == False:
                    years = int(years)
                else:
                    years = np.NaN
                if pd.isna(price) == False:
                    price = int(''.join(re.findall("\d+", price)))
                else:
                    price = np.NaN
                if pd.isna(milage) == False:
                    try:
                        milage_s = re.sub(r'.Km|.km', '', milage)
                    except:
                        milage_s = milage

                to_list = {
                'title': title,
                'price': price,
                'brand' : brand,
                'type' : bike,
                'years': years,
                'milage': milage_s,
                'location': loc,
                'vehicle_type' : 'bike',
                'url' : webpage
                }
                print(to_list, 'page :', i)
                attribute.append(to_list)

attribute = pd.DataFrame(data=attribute)
attribute.to_csv('Output\Early_Bike_Scraped.csv', index=False)