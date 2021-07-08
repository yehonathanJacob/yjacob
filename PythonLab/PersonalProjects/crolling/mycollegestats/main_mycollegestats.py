import os, time

from tqdm import tqdm
import pandas as pd
from selenium import webdriver

import config
import css_selectors

full_df = pd.DataFrame(columns=config.HEADER_COLUMNS + ['College'])

driver = webdriver.Chrome(config.CHROM_DRIVER)
driver.get(config.MAIN_URL)
time.sleep(1)

driver.find_element_by_css_selector(css_selectors.LOGIN_WITH_EMAIL).click()
time.sleep(5)

driver.find_element_by_css_selector(css_selectors.USER_MAIL_BOX).send_keys(config.USER_MAIL)
driver.find_element_by_css_selector(css_selectors.USER_PASSWORD_BOX).send_keys(config.USER_PASSWORD)
driver.find_element_by_css_selector(css_selectors.LOGIN_SUBMIT).click()
time.sleep(5)

select_box = driver.find_element_by_css_selector(css_selectors.SELECT_BOX)
options = [x.get_attribute("value") for x in select_box.find_elements_by_tag_name(css_selectors.COLLEGE_SELECTOR)]

Erorrs = []

for college_name in tqdm(options):
    try:
        if college_name == "":
            continue
        url_to_college = config.URL_TO_COLLEGE.format(college_name=college_name)
        driver.get(url_to_college)
        time.sleep(1)

        driver.execute_script("document.getElementsByTagName('table')[0].style.height = '10000px';")
        driver.execute_script("document.getElementsByTagName('table')[0].style.width = '10000px';")
        time.sleep(1)

        table_body = driver.find_element_by_css_selector(css_selectors.TABLE_BODY)
        data = []

        for row in table_body.find_elements_by_tag_name(css_selectors.TABLE_ROW):
            row_data = [value.text for value in row.find_elements_by_tag_name(css_selectors.TABLE_CELL)]
            data.append(row_data)

        college_df = pd.DataFrame(data, columns=config.HEADER_COLUMNS)
        college_df['College'] = college_name

        full_df = full_df.append(college_df)
    except:
        Erorrs.append(college_name)

driver.quit()

full_df.to_csv(os.path.join(os.getcwd(), 'data.csv'))
