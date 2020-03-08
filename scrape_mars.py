import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup
import time

executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)


def scrape():
    scraped_data = {}
    news_output = mars_news()
    scraped_data['mars_news'] = news_output[0]
    scraped_data['mars_paragraph'] = news_output[1]
    scraped_data['mars_image'] = mars_image()
    scraped_data['mars_weather'] = mars_weather()
    scraped_data['mars_facts'] = mars_facts()
    scraped_data['mars_hemisphere'] = mars_hemisphere()
    return scraped_data


def mars_news():
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    news = soup.find('div', class_='list_text')
    news_title = news.find('div', class_='content_title').text
    news_p = news.find('div', class_='article_teaser_body').text
    news_output = [news_title, news_p]
    return news_output


def mars_image():
    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    image = soup.find('img', class_='thumb')['src']
    featured_image_url = "https://www.jpl.nasa.gov" + image
    return featured_image_url


def mars_weather():
    import tweepy
    auth = tweepy.OAuthHandler(
        'hxQTARtcI6qz5fqtqELao9anB', 'cMRjE4nxWTWQo2PRMKn8wVyrmesQZsCvLRO2QExt3jMCo5XEy8')
    auth.set_access_token('860030876-8TG4lwkS746KEkLDI3iBpC5ggPlIg82TGSHuQyrd',
                          'NBjVOwDYjsvfnL6RPPEiTEpRA47mKR4HYZHPzpePA47Hj')
    api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())
    target_user = 'MarsWxReport'
    tweet = api.user_timeline(target_user, count=1)
    mars_weather = (tweet[0]['text'])
    return mars_weather


def mars_facts():
    facts_url = "https://space-facts.com/mars/"
    browser.visit(facts_url)
    mars_facts = pd.read_html(facts_url)
    mars_facts_df = pd.DataFrame(mars_facts[0])
    mars_facts_df.columns = ['Description', 'Values']
    mars_facts_html = mars_facts_df.to_html(header=False, index=True)
    return mars_facts_html


def mars_hemisphere():
    h_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(h_url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    mars_hemisphere = []
    products = soup.find('div', class_='result-list')
    hemispheres = products.find_all('div', class_='item')
    for hemisphere in hemispheres:
        title = hemisphere.find('h3').text
        title = title.replace('Enhanced', "")
        end_link = hemisphere.find('a')['href']
        image_link = 'https://astrogeology.usgs.gov' + end_link
        browser.visit(image_link)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        downloads = soup.find('div', class_='downloads')
        image_url = downloads.find('a')['href']
        mars_hemisphere.append({'title': title, 'image_url': image_url})
    return mars_hemisphere
