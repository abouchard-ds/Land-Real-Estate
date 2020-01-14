# -*- coding: utf-8 -*-
"""

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
browser.implicitly_wait(4)


# MANAGE THE NUMBER OF PAGES
# <li class="pager-current">
# gives: '1 / 454'
nbpages = browser.find_element_by_xpath("//li[contains(@class, 'pager-current')]").text
# gives: 454
nbpages = nbpages.split()[2]

for curpage in range(1, int(nbpages)):

    print("Doing page " + str(curpage))
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    time.sleep(1.5)
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

df = pd.DataFrame(rows, columns=['description','superficie','prix','ville','fiche','?','link','polldate'])

# BACKUP
df.to_excel("data\\1_Centris_Listing.xlsx",index=False)
del df


###############################################################################
#   Small Data Cleanup
###############################################################################
# reload data from last backup to file
df = pd.read_excel("data\\1_Centris_Listing.xlsx")

# remove bad columns (description, fiche, ?)
df.drop(['description','fiche','?'], axis=1, inplace=True)

# remove missing data (surtout des superficies qui sont vides)
df.dropna(axis=0, how='any', inplace=True)

# remove non-numeric from 'area'
df['superficie'] = df['superficie'].str.replace(r'\D+', '')

# remove non-numeric from 'price'
df['prix'] = df['prix'].str.replace(r'\D+', '')

# type conversion
df["prix"] = pd.to_numeric(df["prix"])
df["superficie"] = pd.to_numeric(df["superficie"])

# remove 'price' au pied carre. genre "5$/ pied carre"
df.drop( df[df['prix']<= 1000], inplace=True)

# ajouter le prix au pied carre
df['prix_au_PC'] = df['prix'] / df['superficie']

# BACKUP
df.to_excel("data\\2_Centris_Listing_Clean.xlsx",index=False)
