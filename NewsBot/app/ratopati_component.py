from RPA.Browser.Selenium import Selenium, By
from qrlib.QRProcess import QRProcess
from qrlib.QRComponent import QRComponent
from qrlib.QRUtils import display
from excelfile import Englishkeywords
import datetime

data = []
keywords = Englishkeywords()
class Ratopati(QRComponent):
    def __init__(self):
        super().__init__()
        self.browser = Selenium()
    def open_broser(self, url):
        display("-----------scraping Ratopati--------------")
        try:
            self.browser.open_available_browser(url, headless=True)
            self.browser.maximize_browser_window()
        except:
            print("Error while opening browser")

    def scrape(self):
        
       
       
        for keyword in keywords:
            print(keyword)
            URL = f"https://english.ratopati.com/search?query={keyword}"
            self.open_broser(URL)

            try:
                maindivs = self.browser.find_elements('//div[@class="post-card__more-secondary-story"]')
                
                for div in maindivs:
                    a_tag = div.find_element(By.TAG_NAME, 'a')
                    Posttime = div.find_element(By.TAG_NAME, 'time')
                    href_value = a_tag.get_attribute('href')
                    title = a_tag.text

                    getTime = (Posttime.text).split(' ')
                    # display(getTime[1])
                    content,time = self.insideLink(href_value)

                    if(getTime[1]=='Minutes' or getTime[1]=='Minute' or getTime[1]=='Seconds' or getTime[1]=='Hour' or getTime[1]=='Hours'):
                        newsData = {'title':title,'date_bs':'', 'date_ad':datetime.datetime.now().strftime("%Y-%m-%d"),'content':content,'keyword':keyword,'newspaper':"Ratopati",'link':href_value }
                    else:
                        break
                data.append(newsData)
            except BaseException as e:
                print(e)
            #display(newsData)
            return data

    def insideLink(self,link):
        self.browser.open_available_browser(link,headless=True)
        self.browser.maximize_browser_window()

        maindiv = self.browser.find_element('//div[@class="content-area"]')
        content = maindiv.find_elements(By.TAG_NAME, 'p')[0].text

        time = self.browser.find_element('//div[@class="author-img flex"]/div').text

        return (content, time)

        



        
        
    
