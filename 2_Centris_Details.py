# -*- coding: utf-8 -*-
"""
Created on Sat Jan 11 01:59:36 2020

@author: captn
"""

import pandas as pd

df = pd.read_excel("data\\2_Centris_Listing_Clean.xlsx")

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

import csv
import time
from datetime import date

today = date.today().strftime('%Y-%m-%d')

options = Options()
options.headless = True

# OPEN BROWSER
# executable_path = r'C:\Utility\BrowserDrivers\geckodriver.exe')
browser = webdriver.Firefox(options=options)
browser.implicitly_wait(4)
time.sleep(2)

rows = []
myline = 1
refresh_count = 1

# REPARTIR A LIGNE 8051 + 621
df_resume = df[ df.index >8673 ]
# TO DO: index 8673 (st-remi) << lui n'etait plus sur Centris et sa brise la loop


# write directly to file instead of a list of list
#with open(r'Terrains_Centris_3.csv', 'a') as f:
#    writer = csv.writer(f)
for l in df_resume['link']:
    
    # FAIRE UNE LOOP POUR REFRESH LE BROWSER APRES 200 QUERY
    # memory montait a 80% apres 200 et rebaisse a 35% apres reboot
    if (refresh_count == 125):
        print("+++++++++++++++++++++++++++++++++++++++++++++++++")
        print("---                 REBOOT                    ---")
        print("+++++++++++++++++++++++++++++++++++++++++++++++++")
        browser.quit()
        time.sleep(3)
        
        browser = webdriver.Firefox(options=options)
        browser.implicitly_wait(4)
        time.sleep(3)

        refresh_count = 1
    
    try:
        # GOTO WEBSITE
        browser.get(l)
        assert "Centris" in browser.title
        time.sleep(1)
        
        row = []
        row.append(browser.find_element_by_xpath("//h2[contains(@itemprop, 'address')]").text)
        row.append(browser.find_element_by_xpath("//.[contains(@id, 'ListingDisplayId')]").text)
        
        # i've seen some without desc which broke the script
        try:
            row.append(browser.find_element_by_xpath("//div[contains(@itemprop, 'description')]").text)
        except:
            row.append("None")
        
        table1 = browser.find_elements_by_xpath("//td[contains(@class, 'last-child')]")
        for line in table1:
            row.append(line.text)
    
        print("--------------- Index is : " + str(myline))  
        print("--------------- Reboot countdown : " + str(125 - refresh_count)) 
        print(row)
    
        myline += 1
        refresh_count += 1
#        writer.writerow(row)
        rows.append(row)
    except:
        print("-----------------------ERREUR--------------------------")
        browser.quit()
        break

# CLOSE BROWSER (va faire une erreur si le nombre d'url est divisible exactement par 200)
browser.quit()

# transform la list de list en df
df2 = pd.DataFrame(rows, columns=['adresse','centris','description','aire','zonage','details'])
        # if break, need a file number and add merge the files by and to ensure correct details
        # df2.to_excel("data\\3_Centris_Details_Part3.xlsx", index=False)

# # write le df
df2.to_excel("data\\3_Centris_Details.xlsx", index=False)

# # Read the csv and cbind to pandas
df3 = pd.concat([df, df2], axis=1, ignore_index=True)
# cols = {0:"Superficie",1:"Prix",2:"Localite",3:"Url",4:"Polldate",5:"Adresse",6:"Centris",7:"Description",8:"Aire",9:"Zonage",10:"Waterfront"}

df3.to_excel("data\\4_Centris_Listing_Plus_Details", index=False)

# 9 066 propriétés trouvées, apres data cleanup le df a 8949 proprietes.
