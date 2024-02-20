from qrlib.QRComponent import QRComponent
from RPA.Browser.Selenium import Selenium

from datetime import datetime
from qrlib.QRUtils import display
import time
from selenium.webdriver.common.by import By

from excelfile import Englishkeywords

keywords = Englishkeywords()



URL="https://thehimalayantimes.com/search?query="
# URL="https://myrepublica.nagariknetwork.com/query"
class Himalayan(QRComponent):
    
    def __init__(self):
        super().__init__()
        self.browser=Selenium()
        
        self.links=[]
        self.news=[]

    def open_browser(self):
        pass

    def scrape(self):
        
        display("-----------scraping himalayan--------------")
        try:
            self.browser.open_available_browser(URL,headless=True)
            self.browser.maximize_browser_window()
        except:
            print("Error in opening the browser")

        try:
            display(keywords)

            for keyword_to_search in keywords:
                items=[]
                self.browser.go_to(URL)
                # display(f"keyword_to_search: {keyword_to_search}")
                self.links=[]
                inputbar = '//input[@class="gnt_se_frm_q"]'
                searchbutton='//button[@class="gnt_se_frm_sm"]'
                self.browser.input_text(inputbar, keyword_to_search)
                display(f"***************Searching for {keyword_to_search} ****************")
                self.browser.click_element(searchbutton)
                time.sleep(5)
                try:
                    articles=self.browser.get_webelements('//div[@class="post_list post_list_style_1"]/article')
                    for article in articles:
                        item={}
                        link_element = article.find_element(By.XPATH, './/h3[@class="alith_post_title"]/a')
                        desc=self.browser.get_text(article.find_element(By.XPATH, './/div[@class="alith_post_except"]'))
                        link = self.browser.get_element_attribute(link_element, 'href')
                        title = self.browser.get_text(link_element)
                        date=self.browser.get_text(article.find_element(By.XPATH, './/span[@class="meta_date"]'))
                        get_time=date.split(" ")
                        item["link"]=link
                        item["title"]=title
                        item["content"]=desc 
                        item["keyword"]=keyword_to_search
                        item["newspaper"]="The Himalayan Times"
                        if(get_time[1]=="H" or get_time[1]=="M" or get_time[1]=="S"):
                            items.append(item)
                            self.links.append(link)
                        else:
                            continue

                    if(len(self.links)>0):
                        for item,link in zip(items,self.links):
                            formatted_date=self.get_details(link)
                            item["date_ad"]=formatted_date
                            item["date_bs"]=""
                            self.news.append(item)
                            display(f"Added Item:{item['title']}")

                    else:
                        display(f"No Links Found for {keyword_to_search}")
                except Exception as e:
                    display(f"Erorr: {e}")

            return self.news

        except Exception as e:
            print(f"Error: {e}")
        
    
    def get_details(self,link):
   
        self.browser.go_to(link)
        time.sleep(1)
        try:
            date_element=self.browser.get_webelement('//div[@class="article_date"]')
            get_date=self.browser.get_text(date_element)
            date_object = datetime.strptime(get_date, 'Published: %I:%M %p %b %d, %Y')
            formatted_date = date_object.strftime('%Y-%m-%d')
        except:
            display("No content")
        return formatted_date
