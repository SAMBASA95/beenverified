import time
import random
import numpy as np
import pandas as pd
from selenium.webdriver.support.ui import Select
from difflib import SequenceMatcher
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import re

chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications": 2}
# DeprecationWarning: use options instead of chrome_options
chrome_options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome('chromedriver.exe', chrome_options=chrome_options)
driver.maximize_window()

# open the webpage
driver.get("https://www.beenverified.com/app/login")
time.sleep(5)

username = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='login-email']")))
password = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='login-password']")))

# enter username and password
username.clear()
username.send_keys('salvep@salvesoft.com')
password.clear()
password.send_keys('Salve123_!')
time.sleep(5)

# target the login button and click it
button = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()
# We are logged in!
time.sleep(15)

# open new window with execute_script()
driver.execute_script("window.open('');")
time.sleep(5)
# switch to new window with switch_to.window()
driver.switch_to.window(driver.window_handles[1])
driver.get("https://www.beenverified.com/app/")
time.sleep(5)

# creating empty array
data_contact = []
data_email = []
data_name = []
data_complete = []
data_address = []
data_social = []


def short_time():
    return random.randint(1, 3)


def long_time():
    return random.randint(5, 11)


def history(driver_search):
    driver_search.execute_script("window.history.go(-1)")


def search(f_name, m_name, l_name, city_name, state_name, driver_search):
    search_people = driver_search.find_element_by_xpath("(//a[@id='peopleTab'])")
    search_people.click()

    time.sleep(short_time())

    first_name = WebDriverWait(driver_search, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='fn']")))
    m_i = WebDriverWait(driver_search, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='mn']")))
    last_name = WebDriverWait(driver_search, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='ln']")))

    city = WebDriverWait(driver_search, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='city']")))

    # state = WebDriverWait(driver_search, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "select[name='state']")))
    state = Select(driver_search.find_element_by_name('state'))

    city.clear()
    first_name.clear()
    m_i.clear()
    last_name.clear()

    first_name.send_keys(f_name)
    m_i.send_keys(m_name)
    last_name.send_keys(l_name)

    if city_name != '':
        city.send_keys(city_name)
    if state_name != '':
        state.select_by_value(state_name)
    # state.send_keys(city_name)
    # state.select_by_value(state_name)

    search_people = WebDriverWait(driver_search, 2).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
    search_people.click()

    while not page_is_loading(driver_search):
        continue

    time.sleep(long_time())

    count_res = driver_search.find_elements_by_xpath("(//a[@class='panel automation-person-result-data-card'])")
    if len(count_res) > 0:
        return True
    else:
        return False


def extraction_20(drive_address):
    while not page_is_loading(drive_address):
        continue

    time.sleep(short_time())
    scr_dis, cur_dis = scroll_search(driver)
    driver.execute_script("window.scrollBy(0, arguments[0]);", scr_dis / 2)
    time.sleep(short_time())
    scr_dis, cur_dis = scroll_search(driver)
    while cur_dis < 1000:
        driver.execute_script("window.scrollBy(0, arguments[0]);", scr_dis / 2)
        scr_dis, cur_dis = scroll_search(driver)

    individual_phone = []
    individual_email = []
    individual_complete = []
    individual_socials = []
    individual_address = []
    dummy_address = []
    data_lead_name = []
    try:
        try:
            data_lead_name = drive_address.find_element_by_xpath(
                "(//div[@class='sidebar_profile__main nav__heading--desktop'])").text
            data_lead_name = data_lead_name.replace("\n", " ")
        except:
            data_lead_name = drive_address.find_element_by_xpath(
                "(//h1[@class='report-header__title'])").text
            data_lead_name = data_lead_name.replace("\n", " ")

        data_lead = drive_address.find_elements_by_xpath("(//a[@class='ember-view title_link'])")
        data_lead_complete = drive_address.find_elements_by_xpath("(//div[@class='report_section__data'])")
        time.sleep(short_time())
        drive_address.execute_script("window.scrollBy(0, arguments[0]);", 6000)

        for ind in data_lead:
            if any(c.isalpha() for c in ind.text):
                if '@' in ind.text:
                    individual_email.append(ind.text)
                    # print(i.text)
            else:
                individual_phone.append(ind.text)
                # print(i.text)

        for j in data_lead_complete:
            line = j.text
            line = line.replace("\n", " ")
            if any(c.isalpha() for c in line):
                if 'https' in line:
                    individual_socials.append(line)
                if 'www.' in line:
                    individual_socials.append(line)

            regexp = "[0-9]{1,7} .+, [A-Z]{2} [0-9]{2,6}"
            if re.findall(regexp, line):
                address = re.findall(regexp, line)
                dummy_address.append(address)
            address = [val for sublist in dummy_address for val in sublist]

            individual_address.append(address)
            individual_address = list(filter(None, individual_address))
            individual_complete.append(line)

        # stop individual search if we find the similar property
        #   for ith_add in address:
        #       if find_seq_ratio(ith_add, address_to_find) > 0.8;
        #         return True

        return individual_complete, individual_address, individual_socials, data_lead_name, individual_phone, individual_email

    except:
        pass

    return individual_complete, individual_address, individual_socials, data_lead_name, individual_phone, individual_email


def get_btn(driver_search):
    report_len_btn = driver_search.find_elements_by_xpath("(//div[@class='card-content'])")
    if len(report_len_btn) > 5:
        return report_len_btn[0:5]
    else:
        return report_len_btn


def find_seq_ratio(found_address, df_address):
    return SequenceMatcher(None, found_address, df_address).ratio()


def scroll_search(driver_search):
    total_hgt = int(driver_search.execute_script("return document.documentElement.scrollHeight"))
    total_Scrolled_Height = int(driver_search.execute_script("return window.pageYOffset + window.innerHeight"))
    return total_hgt, total_Scrolled_Height


# function to check the document is loaded ?
#  wrap , onCanvas are the id's if the page_is_loading get fails
def page_is_loading(driver_tool):
    while True:
        x = driver_tool.execute_script("return document.readyState")
        t_height, c_height = scroll_search(driver_tool)
        if x == "complete" and t_height > 1500:
            return True
        else:
            yield False


main_df = pd.read_excel('demo2.xlsx')
main_df = main_df.replace(np.nan, '', regex=True)

#  report_section__label_title automation-data-card-datapoint
for count in range(0, len(main_df)):
    # Add search person "search" function here -------------
    counter = search(main_df.First_Name[count], main_df.M_Name[count], main_df.Last_Name[count], main_df.City[count],
                     main_df.State[count], driver)
    try:
        if counter:
            get_btn_render = get_btn(driver)
            for i in range(0, len(get_btn_render)):
                time.sleep(short_time())

                get_btn_loop = get_btn(driver)
                if len(get_btn_loop) == 0:
                    search(main_df.First_Name[count], main_df.M_Name[count], main_df.Last_Name[count], main_df.City[count],
                           main_df.State[count], driver)
                    get_btn_loop = get_btn(driver)

                actions = ActionChains(driver)
                actions.move_to_element(get_btn_loop[i]).perform()
                time.sleep(short_time())
                get_btn_loop[i].click()

                while not page_is_loading(driver):
                    continue

                time.sleep(short_time())
                # print('loaded')

                find_address = main_df.Address[count] + " " + main_df.City[count] + " " + main_df.State[count]
                ind_complete, ind_address, ind_socials, ind_lead_name, ind_phone, ind_email = extraction_20(driver)

                data_complete.append(ind_complete)
                data_address.append(ind_address)
                data_social.append(ind_socials)
                data_name.append(ind_lead_name)
                data_contact.append(ind_phone)
                data_email.append(ind_email)

                time.sleep(short_time())

                # complete code for extraction of data
                history(driver)
    except:
        pass
driver.quit()

dummy_tup = tuple(zip(data_complete, data_address, data_social, data_name, data_contact, data_email))
pre_dataFrame = pd.DataFrame(dummy_tup,
                             columns=['data_complete', 'data_address', 'data_social', 'data_name', 'data_contact',
                                      'data_email'])

pre_dataFrame['data_contact'] = pre_dataFrame['data_contact'].astype(str).str.replace(r'\[|\]|', '')
pre_dataFrame['data_email'] = pre_dataFrame['data_email'].astype(str).str.replace(r'\[|\]|', '')
pre_dataFrame['data_address'] = pre_dataFrame['data_address'].astype(str).str.replace(r'\[|\]|', '')
pre_dataFrame['data_social'] = pre_dataFrame['data_social'].astype(str).str.replace(r'\[|\]|', '')

file_name = str(time.time())
pre_dataFrame.to_excel(f'{file_name}.xlsx')
