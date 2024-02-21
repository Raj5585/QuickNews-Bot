from qrlib.QRComponent import QRComponent
from RPA.Browser.Selenium import Selenium
from datetime import datetime
from qrlib.QRUtils import display
import time
from selenium.webdriver.common.by import By

from qrlib.QREnv import QREnv
from excelfile import Englishkeywords

keywords = Englishkeywords()

URL="https://myrepublica.nagariknetwork.com/query"
# URL="https://myrepublica.nagariknetwork.com/query"
class RepublicaComponent(QRComponent):
    
    def __init__(self):
        super().__init__()
        self.browser=Selenium()
        self.links=[]
        self.news=[]

    def scrape(self):
        
        display("******************scraping Republica******************")
        try:
            self.browser.open_available_browser(URL, headless=True)
            self.browser.maximize_browser_window()
        except:
            print("Error in opening the browser")
        try:
            display(keywords)
            for keyword_to_search in keywords:
                self.browser.go_to(URL)
                display(f"keyword_to_search: {keyword_to_search}")
                self.links=[]
                inputbar = '//input[@name="search"]'
                searchbutton='//input[@type="submit"]'
                filter_date='//a[@id="filter24hr"]'
                self.browser.input_text(inputbar, keyword_to_search)
                
                self.browser.click_element(searchbutton)
                time.sleep(5)
                try:
                    aarticle=self.browser.get_webelements('//section[@id="main-hightlight-categories-news"]')
                    time.sleep(5)
                    self.browser.click_element(filter_date)
                    time.sleep(20)
                    articles = self.browser.get_webelements('//div[@class="panel panel-default ajaxResults "]/ul/li[@class="listedResult"]')
                    for article in articles:
                        link_element = article.find_element(By.XPATH, './/h4/a')
                        desc=self.browser.get_text(article.find_element(By.XPATH, './/p[@class="text-default"]'))
                        link = self.browser.get_element_attribute(link_element, 'href')
                        title=self.browser.get_text(article.find_element(By.XPATH, './/h4/a/u'))
                        date=self.browser.get_text(article.find_element(By.XPATH, './/span[@class="smallTag text-muted"]'))
                        get_date = date.split(": ")
                        published_date=get_date[1]
                        date_object = datetime.strptime(published_date[:-16], "%B %d, %Y")
                        formatted_date = date_object.strftime('%Y-%m-%d')
                        
                        self.news.append({'keyword':keyword_to_search,'title': title, 'content':desc,'link': link,'date_bs':'','date_ad':formatted_date,'newspaper':'My Republica'})
                    
                except:
                    display("No Articles")
            return self.news


        except Exception as e:
            print(f"Error: {e}")

        display(f"News: {self.news}")


           