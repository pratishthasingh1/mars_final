# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt

browser = Browser("chrome", executable_path="chromedriver", headless=True)
#^^^ was the first line of the the scrape_all function

def scrape_all():
    # Initiate headless driver for deployment
    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in a dictionary
    nested_data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemis": hemisphere_images(),
        "last_modified": dt.datetime.now() }
    print("BELOW IS THE SCRAPE ALL ------------")
    print(nested_data)
    print("*************************************")
    # Stop webdriver and return data
    browser.quit()
    return nested_data


def mars_news(browser):

    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one("ul.item_list li.slide")
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find("div", class_="content_title").get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find("div", class_="article_teaser_body").get_text()

    except AttributeError:
        return None, None

    return news_title, news_p


def featured_image(browser):
    # Visit URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')[0]
    full_image_elem.click()

    # Find the more info button and click that
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.links.find_by_partial_text('more info')
    more_info_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")

    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'

    return img_url

def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('http://space-facts.com/mars/')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")


def hemisphere_images(): 
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    browser.links.find_by_partial_text("Cerberus").click()
    html = browser.html
    cerberus_soup = soup(html, "html.parser")
    cerberus_titles = cerberus_soup.select_one("div.content h2").text
    cerberus_image= cerberus_soup.select_one("div.downloads a").get("href")

    browser.visit(url)
    browser.links.find_by_partial_text("Schiaparelli").click()
    html = browser.html
    schiaparelli_soup = soup(html, "html.parser")
    schiaparelli_titles = schiaparelli_soup.select_one("div.content h2").text
    schiaparelli_image= schiaparelli_soup.select_one("div.downloads a").get("href")

    browser.visit(url)
    browser.links.find_by_partial_text("Syrtis Major").click()
    html = browser.html
    syrtis_soup = soup(html, "html.parser")
    syrtis_titles = syrtis_soup.select_one("div.content h2").text
    syrtis_image= syrtis_soup.select_one("div.downloads a").get("href") 

    browser.visit(url)
    browser.links.find_by_partial_text("Valles Marineris").click()
    html = browser.html
    valles_soup = soup(html, "html.parser")
    valles_titles = valles_soup.select_one("div.content h2").text
    valles_image= schiaparelli_soup.select_one("div.downloads a").get("href") 

    hemisphere_image_urls = [
        {'cerberus_url': cerberus_image,
        'title': 'Cerberus Hemisphere Enhanced'},
        {'schiaparelli_url': schiaparelli_image,
        'title': 'Schiaparelli Hemisphere Enhanced'},
        {'syrtis_url': syrtis_image,
        'title': 'Syrtis Major Hemisphere Enhanced'},
        {'valles_url': valles_image,
        'title': 'Valles Marineris Hemisphere Enhanced'}]
    print("++++++++++++")
    print(hemisphere_image_urls)
    print("++++++++++++")
    return hemisphere_image_urls


if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())