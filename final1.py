# coding: utf-8

### Flight data record scrapping 

# Imports
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException

import pandas as pd
import string
import csv

# Initializing the browser
path_to_chromedriver = '/home/bt/Documents/Workplace/going_headless/chromedriver/chromedriver'
browser = webdriver.Chrome(executable_path = path_to_chromedriver)

# Headless Browser
chrome_options = webdriver.chrome.options.Options()
chrome_options.add_argument('--headless')
#browser_headless = webdriver.Chrome(executable_path = path_to_chromedriver, chrome_options=chrome_options)
#browser = webdriver.Chrome(executable_path = path_to_chromedriver, chrome_options=chrome_options)

## Get the website 
url = 'https://www.epower.amadeus.com/biscord/#AdtCount=1&CabinClass=&Culture=en-US&DepartureDate=1/18/2018&From=LOS&Method=Search&Page=Result&ProviderList=OnlyAmadeus&ReturnDate=1/30/2018&To=LON'
browser.get(url)

# waiting things
wait = WebDriverWait(browser, 10)

### Functions
# 1. Check if element exist
def elements_exist_by_xpath(xpath):
    try:
        elm = browser.find_elements_by_xpath(xpath)
        #elm.click()
    except NoSuchElementException:
        return False
    return True

# 2. Check if xpath element is visibe/availiabe
def is_available(xpath):
    try:
        element = wait.until(EC.visibility_of_element_located,xpath)
    except:
        return False
    return True

# 3. Extract data from all result element
def get_item_by_xpath(all_res_elem,xpath):
    result = []
    for elm in all_res_elem[:-1]:
        if elm.text != ' ':
            item = elm.find_element_by_xpath(xpath).text
            result.append(item)
    return(result)
# 4.
def get_item_by_xpath2(all_res_elem,xpath):
    result = []
    for elm in all_res_elem[:-1]:
        if elm.text != ' ':
            try:
                item = elm.find_element_by_xpath(xpath).text
                result.append(item)
            except NoSuchElementException:
                try:
                    item = elm.find_element_by_xpath('div/'+xpath).text
                    result.append(item)
                except NoSuchElementException:
                    try:
                        item = elm.find_element_by_xpath('div/div/'+xpath).text
                        result.append(item)
                    except NoSuchElementException:
                        try:
                            item = elm.find_element_by_xpath('div/div/div/'+xpath).text
                            result.append(item)
                        except NoSuchElementException:
                            result.append('not available')
                
    return(result)



# Results panal
xpaths = '//*[@id="Obj_Result"]/div/div[3]/div'


# Check Wrapping
# Check if the path is available
if is_available(xpaths):
    # check elements existence
    if elements_exist_by_xpath(xpaths):
        #print("...Results Present")
        # Get all result element
        print('...acquiring reseult panal element')
        all_elem = browser.find_elements_by_xpath(xpaths)
        # Check if the list isn't empty
        if len(all_elem) > 0:
            print("...{} Result Element acquired".format(len(all_elem)))
        else:
            print("...{} Result Element acquired".format(len(all_elem)))
else:
    print('No Result Panel')


### Data Acquisition
# Query starts

# Airline list
airline_xpath = 'div[1]/div/div/div[1]/div/div[1]'
airline_list = get_item_by_xpath(all_elem,airline_xpath)
#airline_list
# Price list
price_xpath = 'div[1]/div/div/div[3]/div[2]/div/div/div[1]/div[2]'
price_list = get_item_by_xpath(all_elem,price_xpath)
price_list
# Number of seats left list
no_seat_left_xpath = 'div[1]/div/div/div[3]/div[2]/div/div/div[1]/div[1]/label'
no_seats_left_list = get_item_by_xpath(all_elem,no_seat_left_xpath)
no_seats_left_list
# Time of Travel list
time_traveld_xpath = 'div/div/div/div[1]/div/div[2]/div[2]/div[2]/div/div[2]/span'
time_traveld_list = get_item_by_xpath2(all_elem,time_traveld_xpath)
#time_traveld_list
# arrival
arr_time_xpath = 'div[1]/div/div/div[1]/div/div[2]/div[2]/div[2]/div/div[3]/div/div/div'
arr_time_list = get_item_by_xpath2(all_elem,arr_time_xpath)
#arr_time_list
# Destination info
to_loc_xpath = 'div[1]/div/div/div[1]/div/div[2]/div[2]/div[2]/div/div[3]/div/div/span[1]'
to_loc_list = get_item_by_xpath2(all_elem,to_loc_xpath)
#to_loc_list
# depture_time
dep_time_xpath = 'div[1]/div/div/div[1]/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div'
dep_time_list = get_item_by_xpath2(all_elem,dep_time_xpath)
#dep_time_list
# from
from_xpath = 'div[1]/div/div/div[1]/div/div[2]/div[2]/div[2]/div/div[1]/div/div/span[1]'
from_list = get_item_by_xpath2(all_elem,from_xpath)
#from_list
# Number of stops
num_stops_xpath = 'div[1]/div/div/div[1]/div/div[2]/div[2]/div[2]/div/div[2]/div'
num_stops_list = get_item_by_xpath2(all_elem,num_stops_xpath)
#num_stops_list

# Querry Ends


### Data Processing and Structuring

# Processes Price
price1_list = []
price2_list = []

for p in price_list:
    a = p.split('\n')
    price1_list.append(a[0])
    if len(a)>1:
        price2_list.append(a[1])
    else:
        price2_list.append("")

# Structuring the data
col_name =['Airline','From','Dep_time','To','Arr_time','Num_stops','No_seats','Price1','Price2']
structured_dict = {'Airline':airline_list,'From':from_list,
                   'Dep_time':dep_time_list,'To':to_loc_list,
                   'Arr_time':arr_time_list,'Num_stops':num_stops_list,
                   'Num_seats':no_seats_left_list,'Price1':price1_list,'Price2':price2_list}

str_data = pd.DataFrame(structured_dict)
str_data.to_csv('fligthRec.csv',header=True,index=False,columns=col_name)


