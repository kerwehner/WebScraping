
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd


def scrape():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    browser = Browser("chrome", **executable_path, headless=False)

    news_title, news_p = mars_news(browser)
    data = {
        'news_title': news_title,
        'news_p': news_p,
        # 'featured_image': feature_image(browser),
        # 'weather': twitter_weather(browser),
        'facts': mars_facts(),
        'hemisphere': hemisphere_image_urls(browser)
    }
    return data

def mars_news(browser):

    # NASA Mars News Titles
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=0.5)
    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    news_soup = bs(html, 'html.parser')
    try: 
        slide_element = news_soup.select_one("ul.item_list li.slide")
        latest_news_title = slide_element.find("div", class_="content_title").get_text()
        news_paragraph = slide_element.find("div", class_="article_teaser_body").get_text()

    except AttributeError:
        return None, None
    return latest_news_title, news_paragraph
    
def mars_facts():
        try:
            mars_df = pd.read_html("https://space-facts.com/mars/")[0]
        except BaseException:
            return None
        mars_df.columns = ["Description", "Value"]
        mars_df.set_index("Description", inplace = True)
        return mars_df.to_html(classes="table table-striped")

def hemisphere_image_urls(browser):
        url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(url)
        hemisphere_image_urls = []
        links = browser.find_by_css("a.product-item h3")
        for item in range(len(links)):
            hemisphere = {}
            browser.find_by_css("a.product-item h3")[item].click()
            sample_element = browser.find_by_text("Sample").first 
            hemisphere["img_url"]=sample_element["href"]
            hemisphere["title"]=browser.find_by_css("h2.title").text 
            hemisphere_image_urls.append(hemisphere)
            browser.back()
        return hemisphere_image_urls
   
def scrape_hemisphere(html_text):
    hemisphere_soup = bs(html_text, "html.parser")
    try:
        title_element = hemisphere_soup.find("h2", class_="title").get_text()
        sample_element = hemisphere_soup.find("a", text="Sample").get("href")
    except AttributeError:
        title_element = None
        sample_element = None
    hemisphere = {
        "title": title_element,
        "img_url": sample_element,
    }
    return hemisphere
if __name__ == "__main__":
    print(scrape())
    
    # # Mars Hemispheres
    # url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    # title=[]
    # response = browser.visit(url)
    # soup = bs(browser.html, 'html.parser')
    # titles_list = soup.find_all('div', class_='description')
    # for titles in titles_list:
    #     t = titles.h3.text
    #     title.append(t)

    # urls_list=['https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced',
    #             'https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced',
    #             'https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced',
    #             'https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced']
    # image_url=[]
    # for urls in urls_list:
    #     url = urls
    #     response = browser.visit(url)
    #     time.sleep(3)
    #     soup = bs(browser.html, 'html.parser')
    #     image = soup.find('a', text="Sample")
    #     print(image)
    #     image_link = image.get('href')
    #     image_url.append(image_link)

    # hemisphere_image_urls=[]
    # for i in range(len(title)):
    #     d = dict([('title', title[i]), ('img_url', image_url[i])])
    #     hemisphere_image_urls.append(d)

    # # # Create combine dict
    # mars_data = {
    #     'latest_title': article_title,
    #     'latest_paragraph': article_p,
    #     'data_table': mars_df_html,
    #     'hemisphere': hemisphere_image_urls
    # }
    # return (mars_data)