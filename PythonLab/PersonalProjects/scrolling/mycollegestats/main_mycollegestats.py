import time

from tqdm import tqdm
import pandas as pd
from selenium import webdriver


CHROM_DRIVER = '/home/yjacob/Documents/drivers/chromedriver'
MAIN_URL = 'https://www.mycollegestats.com/output'
USER_MAIL = 'yehonathanjacob@gmail.com'
USER_PASSWORD = 'test123'

HEADER_COLUMNS = ['Year Applied', 'School Name', 'Visited', 'Sex', 'Year of Birth', 'Race', 'Country of Citizenship', 'Country of Residence', 'State of Residence', '1st Language', '2nd Language', 'High School', 'U/W GPA', 'GPA Max', 'SAT Math', 'SAT Reading', 'SAT Total', 'ACT', 'Essay', 'SAT II Subject', 'SAT II Score', 'SAT II Subject', 'SAT II Score', 'College Decision', 'Student Decision']

full_df = pd.DataFrame(columns=HEADER_COLUMNS+['College'])

driver = webdriver.Chrome(CHROM_DRIVER)
driver.get(MAIN_URL)
time.sleep(1)

driver.find_element_by_css_selector('button._1_kc0').click()
time.sleep(5)

driver.find_element_by_css_selector('input#input_input_emailInput_SM_ROOT_COMP1').send_keys(USER_MAIL)
driver.find_element_by_css_selector('input#input_input_passwordInput_SM_ROOT_COMP1').send_keys(USER_PASSWORD)
driver.find_element_by_css_selector('button._1_kc0').click()
time.sleep(5)

select_box = driver.find_element_by_css_selector('select#comp-k8xo0cp7collection')
options = [x.get_attribute("value") for x in select_box.find_elements_by_tag_name("option")]

Erorrs = []

for college_name in tqdm(options):
    try:
        if college_name == "":
            continue
        url_to_college = f'https://www.mycollegestats.com/applicationresult/{college_name}'
        driver.get(url_to_college)
        time.sleep(1)

        driver.execute_script("document.getElementsByClassName('_3GbbP')[0].style.height = '10000px';")
        driver.execute_script("document.getElementsByClassName('_3GbbP')[0].style.width = '10000px';")
        time.sleep(1)

        table_body = driver.find_element_by_css_selector('tbody._1q39m._1zrpA._3lT4j')
        data = []

        for row in table_body.find_elements_by_tag_name("tr"):
            row_data = [value.text for value in row.find_elements_by_tag_name("td")]
            data.append(row_data)

        college_df = pd.DataFrame(data, columns=HEADER_COLUMNS)
        college_df['College'] = college_name

        full_df = full_df.append(college_df)
    except:
        Erorrs.append(college_name)


driver.quit()

full_df.to_excel('/home/yjacob/repos/yjacob/PythonLab/PersonalProjects/scrolling/mycollegestats/data.xlsx')
