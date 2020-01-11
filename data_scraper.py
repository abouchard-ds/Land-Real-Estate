# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 22:56:51 2020

@author: captn
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options

import time
import pandas as pd
from datetime import date

today = date.today().strftime('%Y-%m-%d')

options = Options()
options.headless = True

# OPEN BROWSER
# executable_path = r'C:\Utility\BrowserDrivers\geckodriver.exe')
browser = webdriver.Firefox(options=options)
browser.implicitly_wait(2)

rows = []

# GOTO WEBSITE
browser.get("https://www.centris.ca/fr/terrain~a-vendre?view=List")
assert "Centris" in browser.title
browser.implicitly_wait(2)


# MANAGE THE NUMBER OF PAGES
# <li class="pager-current">
# gives: '1 / 454'
nbpages = browser.find_element_by_xpath("//li[contains(@class, 'pager-current')]").text
# gives: 454
nbpages = nbpages.split()[2]

for curpage in range(1, int(nbpages)):

    print("Doing page " + str(curpage))
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    time.sleep(0.5)
    terrains = browser.find_elements_by_xpath("//div[contains(@class, 'row templateListItem')]")
    links = browser.find_elements_by_xpath("//a[contains(@class, 'btn a-more-detail')]")
    
    # 20 records par page
    i = 0
    for terrain in terrains:
        row = terrain.text.splitlines()             # string to list splitted on new line
        row.append(links[i].get_attribute('href'))  # add corresponding link
        row.append(today)                           # add the poll date to the record
        print(row)                                  # validation
        rows.append(row)                            # add to list of list
        i += 1
        print("--------------------------------------------------------------------")

    # Next page
    time.sleep(0.5)
    btnnext = browser.find_element_by_xpath("//li[contains(@class, 'next')]")
    btnnext.click()
    
# CLOSE BROWSER

browser.quit()

df = pd.DataFrame(rows, columns=['description','area','price','address','fiche','?','link','polldate'])

# SAVE DATA TO FILE
df.to_excel("Terrains_Centris_Clean.xlsx",index=False)
