import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from models import Post
from abc import ABC, abstractmethod


class BaseScraper(ABC):
  future_posts = []

  headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
  }
    
  def add_post(self,post):
    self.future_posts.append(post)

  @abstractmethod
  def scrape_one_page():
    pass

  @abstractmethod
  def scrape_all_pages():
    pass

  @abstractmethod
  def create_posts_from_html():
    pass

  

class WebScraper(BaseScraper):
  webscraper_base_url = 'https://webscraper.io/test-sites/e-commerce/static'
  webscraper_relative_urls = ['/test-sites/e-commerce/static/computers/laptops','/test-sites/e-commerce/static/computers/tablets','/test-sites/e-commerce/static/phones/touch']

  def create_posts_from_html(self,soup):
    scraped_info = soup.find_all('div',class_='caption')
    for el in scraped_info:
      price = el.find('h4',class_='price').text
      title = el.find('a',class_='title').text
      description = el.find('p',class_='description').text
      post = Post(title=f"{title} {price}",body=description,owner_id=1)
      self.add_post(post)

  def scrape_one_page(self,url):
    page = requests.get(url,headers=self.headers)
    soup = BeautifulSoup(page.text, 'html.parser')
    self.create_posts_from_html(soup)
    next_page_link = soup.find('a',class_='page-link',attrs={'rel':'next'})
    return next_page_link

  def scrape_all_pages(self,url):
    next_page_link = self.scrape_one_page(url)
    while next_page_link != None:
      next_page_url = urljoin(url, next_page_link['href'])
      next_page_link = self.scrape_one_page(next_page_url)

  def scrape_webscraper(self):
    for relative_url in self.webscraper_relative_urls:
      url_to_scrap = urljoin(self.webscraper_base_url,relative_url)
      self.scrape_all_pages(url_to_scrap)
 

  

class ToScrape(BaseScraper):
  toscrape_base_url = 'https://books.toscrape.com/catalogue/'
  toscrape_page1_url = toscrape_base_url + 'page-1.html'

  def create_posts_from_html(self,soup):
    links_to_books = soup.select('.image_container a')
    for link in links_to_books:
      url = urljoin(self.toscrape_base_url,link['href'])
      post = self.create_post_from_book_on_page(url)
      self.add_post(post)

  def create_post_from_book_on_page(self,url):
    page = requests.get(url,headers=self.headers)
    soup = BeautifulSoup(page.text, 'html.parser')
    title_element = soup.select_one('.product_main h1')
    body_element = soup.select_one('.product_page > p')
    if title_element and body_element:
      title = title_element.text
      body = body_element.text
      post = Post(title,body,owner_id=1)
      return post

  def scrape_one_page(self,url):
    page = requests.get(url,headers=self.headers)
    soup = BeautifulSoup(page.text, 'html.parser')
    self.create_posts_from_html(soup)
    next_page_link = soup.find('li',class_='next')
    return next_page_link

  def scrape_all_pages(self):
    next_page_link = self.scrape_one_page(self.toscrape_page1_url)
    while next_page_link != None:
      next_page_url = urljoin(self.toscrape_base_url, next_page_link.find('a')['href'])
      next_page_link = self.scrape_one_page(next_page_url)
