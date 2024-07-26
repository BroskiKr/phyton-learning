import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from abc import ABC, abstractmethod
from schemas import NewPost

class BaseScraper(ABC):
  future_posts = []

  headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
  }
    
  def add_post(self,post):
    self.future_posts.append(post)

  def scrape_one_page(self,url,next_page_link_find_params):
    page = requests.get(url,headers=self.headers)
    soup = BeautifulSoup(page.text, 'html.parser')
    self.create_posts_from_html(soup)
    next_page_link = soup.find(**next_page_link_find_params)
    return next_page_link

  def scrape_all_pages(self,url,next_page_link_find_params):
    next_page_link = self.scrape_one_page(url,next_page_link_find_params)
    while next_page_link != None:
      if next_page_link_find_params['name'] == 'a':
        next_page_url = urljoin(url, next_page_link['href'])
      else:
        next_page_url = urljoin(url, next_page_link.find('a')['href'])
      next_page_link = self.scrape_one_page(next_page_url,next_page_link_find_params)

  @abstractmethod
  def create_posts_from_html():
    pass

  @abstractmethod
  def scrape():
    pass


  
class WebScraper(BaseScraper):
  webscraper_base_url = 'https://webscraper.io/test-sites/e-commerce/static'
  webscraper_relative_urls = ['/computers/laptops','/computers/tablets','/phones/touch']

  next_page_link_find_params = {
      'name':'a',
      'class_':'page-link',
      'attrs':{'rel':'next'}
    }

  def create_posts_from_html(self,soup):
    scraped_info = soup.find_all('div',class_='caption')
    for el in scraped_info:
      price = el.find('h4',class_='price').text
      title = el.find('a',class_='title').text
      description = el.find('p',class_='description').text
      post = NewPost(title=f"{title} {price}",body=description,owner_id=1)
      self.add_post(post)

  def scrape(self):
    for relative_url in self.webscraper_relative_urls:
      url_to_scrap = self.webscraper_base_url + relative_url
      self.scrape_all_pages(url_to_scrap,self.next_page_link_find_params)

 

class ToScrape(BaseScraper):
  toscrape_base_url = 'https://books.toscrape.com/catalogue/page-1.html'

  next_page_link_find_params = {
      'name':'li',
      'class_':'next',
    }

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
      post = NewPost(title=title,body=body,owner_id=1)
      return post
    
  def scrape(self):
    self.scrape_all_pages(self.toscrape_base_url,self.next_page_link_find_params)





