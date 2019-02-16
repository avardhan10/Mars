# Import Dependencies 
import os
import pandas as pd
from bs4 import BeautifulSoup
from splinter import Browser
from selenium import webdriver
import requests
import time
import datetime as dt

def scrape_all():
	
    exec_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', headless=True, **exec_path)

    data = {
        "news_title": scrape_mars_news(browser)[0],
        "news_paragraph": scrape_mars_news(browser)[1],
        "featured_image": scrape_mars_image(browser),
        "hemispheres": scrape_mars_hemispheres(browser),
        "weather": scrape_mars_weather(browser),
        "facts": scrape_mars_facts(),
        "last_modified": dt.datetime.now()
    }


    return data

# NASA MARS NEWS
def scrape_mars_news(browser):

    mars_info = {}

    # Visit Nasa news url through splinter module
    nasa_url_news = 'https://mars.nasa.gov/news/'
    browser.visit(nasa_url_news)

    # HTML Object
    html = browser.html

    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html,'html.parser')

    # Scraping the NASA Mars News Site contains news title and news paragraph
    news_title = soup.find('div', class_='content_title').find('a').text
    news_paragraph = soup.find('div', class_='rollover_description_inner').text

    # Dictionary entry from MARS NEWS
    mars_info['news_title'] = news_title
    mars_info['news_paragraph'] = news_paragraph

    return news_title, news_paragraph

   # finally:

    #    browser.quit()

# FEATURED IMAGE
def scrape_mars_image(browser):

        #browser.is_element_present_by_css("img.jpg", wait_time=1)

    # Visit Mars Space Images through splinter module
    featured_image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(featured_image_url)
    # HTML Object
    html_image = browser.html

    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html_image, 'html.parser')

    # Retrieving background image URL from the style tag
    featured_image_url  = soup.find('article')['style']
    featured_image_url = featured_image_url.split("'")
    featured_image_url = featured_image_url[1]
    base_url = 'https://www.jpl.nasa.gov'
    image_url = base_url + featured_image_url

    return image_url
        
#    finally:

 #       browser.quit()

# Mars Weather 
def scrape_mars_weather(browser):

        #browser.is_element_present_by_css("div", wait_time=1)

    # Visit Mars Weather Twitter through splinter module
    weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(weather_url)

    # HTML Object
    html_weather = browser.html

    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html_weather, 'html.parser')

    # Find all elements that contain tweets
    latest_tweets = soup.find_all('p', class_='tweet-text')

    weather = ''

    for tweet_html in latest_tweets:
        tweet_html = tweet_html.text.strip()
        if tweet_html.startswith('Sol'):
            weather = weather + f' {tweet_html}'
 
    return weather[:96]
    #finally:

     #   browser.quit()

        # Mars Facts
def scrape_mars_facts():

    # Visit Mars facts url 
     facts_url = 'http://space-facts.com/mars/'

     table = pd.read_html(facts_url)
     mars_df = table[0]
     mars_df.columns = ['Mars Planet Profile', 'Value']

     return mars_df.to_html(classes='table table-striped')

# MARS HEMISPHERES


def scrape_mars_hemispheres(browser):

    # Visit hemispheres website through splinter module
    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres_url)

    # HTML Object
    html_hemispheres = browser.html

    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html_hemispheres, 'html.parser')

    # Retreive all items that contain mars hemispheres information
    items = soup.find_all('div', class_='item')

    # Create empty list for hemisphere urls
    hemisphere_image_url = []

    # Store the main_ul
    hemispheres_main_url = 'https://astrogeology.usgs.gov'

    # Loop through the items previously stored
    for i in items:
        # Store title
        title = i.find('h3').text

        # Store link that leads to full image website
        partial_img_url = i.find('a', class_='itemLink product-item')['href']

        # Visit the link that contains the full image website
        browser.visit(hemispheres_main_url + partial_img_url)

        # HTML Object of individual hemisphere information website
        partial_img_html = browser.html

        # Parse HTML with Beautiful Soup for every individual hemisphere information website
        soup = BeautifulSoup( partial_img_html, 'html.parser')

        # Retrieve full image source
        image_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']

        # Append the retreived information into a list of dictionaries
        hemisphere_image_url.append({"title" : title, "img_url" : image_url})

    return hemisphere_image_url
    #finally:

     #   browser.quit()

