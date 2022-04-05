# encoding:UTF-8
import re
import datetime
import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

category_id = ['twentyFourHourButton', 'sevenDaysButton', 'thirtyDaysButton', 'allTimeButton']
table_id = ['table', 'table24Hours', 'table24Hours', 'table24Hours']
file_id = ['24 Hours', '7 days', '30 days', 'All time']
next_id = ['table_next', 'table24Hours_next', 'table24Hours_next', 'table24Hours_next']
table_columns = ['', 'Collection', 'Sales USD', 'Buyers', 'Sellers', 'Transactions']

url = "https://cryptoslam.io/nfts#"


def find_all_category():
    option = webdriver.ChromeOptions()
    option.add_argument('headless')

    browser = webdriver.Chrome(options=option)
    browser.implicitly_wait(30)
    browser.get(url)

    time.sleep(5)
    locator = ("xpath", '//table[@id="table"]')
    WebDriverWait(browser, 10).until(ec.presence_of_all_elements_located(locator), 'Could not load page')

    time_id = 0
    while time_id < 3:
        file_name = file_id[time_id] + "-" + str(datetime.date.today()) + ".csv"

        button = browser.find_element(By.XPATH, '//button[@id="' + category_id[time_id] + '"]')
        button.click()

        locator = ("xpath", '//table[@id="' + table_id[time_id] + '"]')
        WebDriverWait(browser, 20).until(ec.presence_of_all_elements_located(locator), 'Could not load page')

        column_lists = []
        page_id = 0
        while page_id < 4:
            # WebDriverWait(browser, 10).until(lambda browser: browser.find_element_by_id('table'))

            data = browser.find_element(By.ID, table_id[time_id]).text
            data = str(data)

            pattern = '\n(.*)'
            my_string = re.findall(pattern, data)

            i = 0

            while i < len(my_string):
                row_data = my_string[i]

                column_list = []
                row_value = row_data.split(' ')
                column_list.append(row_value[0])

                name_pattern = '  (.*) \\$'
                name_value = re.findall(name_pattern, row_data)
                if len(name_value) < 1:
                    break
                column_list.append(name_value[0])

                pivot = len(str(name_value[0]).split(' '))

                if row_value[1 + pivot + 2] == '-':
                    column_list.append(row_value[1 + pivot + 1])
                    column_list.append(row_value[1 + pivot + 5])
                    column_list.append(row_value[1 + pivot + 7])
                    column_list.append(row_value[1 + pivot + 9])
                elif row_value[1 + pivot + 7] == '-':
                    column_list.append(row_value[1 + pivot + 1])
                    column_list.append(row_value[1 + pivot + 6])
                    column_list.append(row_value[1 + pivot + 8])
                    if row_value[1 + pivot + 9] == '-':
                        column_list.append(row_value[1 + pivot + 10])
                    else:
                        column_list.append(row_value[1 + pivot + 11])
                elif row_value[1 + pivot + 10] == '-':
                    column_list.append(row_value[1 + pivot + 1])
                    column_list.append(row_value[1 + pivot + 6])
                    column_list.append(row_value[1 + pivot + 9])
                    column_list.append(row_value[1 + pivot + 11])
                elif len(row_value) <= 1 + pivot + 12:
                    column_list.append(row_value[1 + pivot + 1])
                    column_list.append(row_value[1 + pivot + 6])
                    column_list.append(row_value[1 + pivot + 8])
                    column_list.append(row_value[1 + pivot + 10])
                else:
                    column_list.append(row_value[1 + pivot + 1])
                    column_list.append(row_value[1 + pivot + 6])
                    column_list.append(row_value[1 + pivot + 9])
                    column_list.append(row_value[1 + pivot + 12])

                column_lists.append(column_list)
                i += 1

            pagination_button = browser.find_element(By.ID, next_id[time_id]).find_element(By.TAG_NAME, "a")
            pagination_button.click()
            page_id += 1

        with open(file_name, "w", newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(table_columns)
            writer.writerows(column_lists)
        print("Time table:" + file_id[time_id] + "" + " completed!")
        time_id += 1
    browser.quit()


if __name__ == "__main__":
    find_all_category()
    print("HelloWorld")
