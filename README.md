# Land_Robot
Data Analysis for Land Purchase

![Boreal Forest](/media/myboreal.jpg)

I want to buy land in the boreal forest. So I made a scraper to get me the data, then a data cleaner. Then I do some data analysis on the properties with using business analytics and machine learning. 

## Web scraper 'List' and 'Detail'

The web scraping is done in 2 parts.

First I get the listing of all land for sale which provide me with basic info (area,price,town) AND the links for each listing. Then I scrape each individual listing to get the detailed information.

I started with my usual `bs4`, but could not get the page to switch because there are no page numbers in the URL of the website. So I had to learn `Selenium` from scratch. First I wanted to use `Selenium` only for page switching thus reusing what I already developed but the `driver.page_source` method seems to truncate the page and I consistently got only 12 results instead of the 20 per pages I was suposed to get.

### Methodology

1. Connect to the website (url include land properties only)
2. Get the number of pages for the loop
3. Get the data and the link for the 20 properties on the page
4. Do this for all the pages
5. Write the data to disk (Excel)

*Got the data from 453 pages453 pages to analyze 9061 properties.*

## Further data augmentation

I'm getting the distance from my home for each land property using the Google Map API since I'm only interested in land not further than 2 driving hours. 

I'm adding meteorological and geological data because it is important for my purpose.


## Data Cleanup

Nothing special.


## Analysis


# ML

