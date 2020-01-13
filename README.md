# Land Real Estate Program
Proof of concept.

![Boreal Forest](/media/myboreal.jpg)

I want to buy land in the boreal forest. No website offer me the information I want.

- I want good current data on the market to make informed decisions;
- I want to be able to compare listings side by side;
- I want to query the data, I dont want to endlessly check on very basic webpages;
- I want to find anomalies in the market to benefit from;
- I want to know which properties are in a positive cashflow where applicable;
- I want to study which factors are i fluencing the price;
- I want to know which proportion on listings say they are "rare" opportunities;
- I want to know what is the average price per square foot on a given region;

The website I've checked has nothing of the sort. It's like it was developped by a children: extremely basic, nothing really usefull.

So I made a scraper to get the data. And then I augment it with other data sources.

## Web scraper 'List' and 'Detail'

The web scraping is done in multiple parts.

First I get the listing of all land for sale which provide me with basic info (area,price,town) AND the links for each listing. Then I scrape each individual listing to get the detailed information.

I started with my usual `bs4`, but could not get the page to switch because there are no page numbers in the URL of the website. So I had to learn `Selenium` from scratch. First I wanted to use `Selenium` only for page switching thus reusing what I already developed but the `driver.page_source` method seems to truncate the page and I consistently got only 12 results instead of the 20 per pages I was suposed to get.

### Methodology

1. Connect to the website (url include land properties only)
2. Get the number of pages for the loop
3. Get the data and the link for the 20 properties on the page
4. Do this for all the pages
5. Write the data to disk (Excel)
6. Add other sources

*Got the data from 453 pages to analyze 9061 properties.*

## Further data augmentation

I'm getting the distance from my home for each land property using the Google Map API since I'm only interested in land not further than 2 driving hours. 

I'm adding meteorological and geological data because it is important for my purpose.

Add gmap distance matrix from home.

Add gmap geoloc data.

Plant Hardiness zone.

2016 census data.

Cartographie hydrogeologique.



## Data Cleanup

Nothing special. Extracting postal  code for use with googlemap api. 


## Analysis

Factors most contributing to the price.

Heatmap of price per square foot.

Listing land that are under 2h from home, with low prices.

Checking land with aberrant prices. If i missed something find other similar that are not expensive.

# ML

Regression pour savoir le prix que devrais etre un terrain.
