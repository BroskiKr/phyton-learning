import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

future_posts = []

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
}

webscraper_base_url = 'https://webscraper.io/test-sites/e-commerce/static'

webscraper_relative_urls = ['/test-sites/e-commerce/static/computers/laptops','/test-sites/e-commerce/static/computers/tablets','/test-sites/e-commerce/static/phones/touch']


def create_posts_webscraper(soup):
  scraped_info = soup.find_all('div',class_='caption')
  for el in scraped_info:
    price = el.find('h4',class_='price').text
    title = el.find('a',class_='title').text
    description = el.find('p',class_='description').text
    future_posts.append({'title':f"{title} {price}",'body':description})

def scrape_webscraper_page(url):
  page = requests.get(url,headers=headers)
  soup = BeautifulSoup(page.text, 'html.parser')
  create_posts_webscraper(soup)
  next_page_link = soup.find('a',class_='page-link',attrs={'rel':'next'})
  while next_page_link != None:
    next_page_url = urljoin(url, next_page_link['href'])
    page = requests.get(next_page_url,headers=headers)
    soup = BeautifulSoup(page.text, 'html.parser')
    create_posts_webscraper(soup)
    next_page_link = soup.find('a',class_='page-link',attrs={'rel':'next'})

for relative_url in webscraper_relative_urls:
  url_to_scrap = urljoin(webscraper_base_url,relative_url)
  scrape_webscraper_page(url_to_scrap)


toscrape_base_url = 'https://books.toscrape.com/catalogue/'

toscrape_page1_url = toscrape_base_url + 'page-1.html'

def create_posts_toscrape(soup):
  links_to_book = soup.select('.image_container a')
  for link in links_to_book:
    url = urljoin(toscrape_base_url,link['href'])
    page = requests.get(url,headers=headers)
    soup = BeautifulSoup(page.text, 'html.parser')
    title_element = soup.select_one('.product_main h1')
    body_element = soup.select_one('.product_page > p')
    if title_element and body_element:
      title = title_element.text
      body = body_element.text
      future_posts.append({'title': title, 'body': body})


def scrape_toscrape_page(url):
  page = requests.get(url,headers=headers)
  soup = BeautifulSoup(page.text, 'html.parser')
  create_posts_toscrape(soup)
  next_page_link = soup.find('li',class_='next')
  while next_page_link != None:
    next_page_url = urljoin(url, next_page_link.find('a')['href'])
    page = requests.get(next_page_url,headers=headers)
    soup = BeautifulSoup(page.text, 'html.parser')
    create_posts_toscrape(soup)
    next_page_link = soup.find('li',class_='next')

scrape_toscrape_page(toscrape_page1_url)


