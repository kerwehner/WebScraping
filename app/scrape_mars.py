
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd
import re


def init_browser():
    executable_path = {"executable_path": "C://Program Files/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()

    # NASA Mars News Titles
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")
    article_title = soup.find("div", class_='content_title').text.strip()

    # NASA Mars News Text
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    article_p = soup.find('div', class_='rollover_description_inner').text.strip()

    # Mars Facts
    mars_df = pd.read_html('http://space-facts.com/mars/',attrs={'id':'tablepress-p-mars-no-2'})
    mars_df = mars_df[0]
    mars_df.columns = ["Category", "Data"]
    mars_df_html = mars_df.to_html(index = False)
    
    
    # Mars Hemispheres
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    title=[]
    response = browser.visit(url)
    soup = bs(browser.html, 'html.parser')
    titles_list = soup.find_all('div', class_='description')
    for titles in titles_list:
        t = titles.h3.text
        title.append(t)

    urls_list=['https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced',
                'https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced',
                'https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced',
                'https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced']
    image_url=[]
    for urls in urls_list:
        url = urls
        response = browser.visit(url)
        soup = bs(browser.html, 'html.parser')
        image = soup.find('a', attrs={'target&v1':'_blank', 'href': re.compile('^http://')})
        image_link = image.get('href')
        image_url.append(image_link)

    hemisphere_image_urls=[]
    for i in range(len(title)):
        d = dict([('title', title[i]), ('img_url', image_url[i])])
        hemisphere_image_urls.append(d)

    # # Create combine dict
    mars_data = {
        'latest_title': article_title,
        'latest_paragraph': article_p,
        'data_table': mars_df_html,
        'hemisphere': hemisphere_image_urls
    }
    return (mars_data)