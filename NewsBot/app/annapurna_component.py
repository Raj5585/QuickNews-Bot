from qrlib.QRComponent import QRComponent
from RPA.Browser.Selenium import Selenium
import time
from qrlib.QRUtils import display
import nepali_datetime
import date_utils
from excelfile import Nepalikeywords

keywords = Nepalikeywords()
class AnnapurnaComponent(QRComponent):
    
    def __init__(self):
        super().__init__()
        self.browser = Selenium()
        self.url = "https://www.annapurnapost.com/search"
        self.links = []
        self.nepali_date=nepali_datetime.date.today().strftime('%Y-%m-%d')
        self.results = []

    def open_browser(self):
        pass

    def scrape(self):
        
        display("-----------scraping Annapurna--------------")
        try:
            self.browser.open_available_browser(self.url, headless=True)
            self.browser.maximize_browser_window()
            time.sleep(2)
        except Exception as e:
            print(f"Error: {e}")

        total_count = 0
        # Perform a search for each keyword
        for keyword in keywords:
            display(f"***************Searching for {keyword} *****************")
            links = []
            search_url=f"{self.url.strip()}?q={keyword}"
            self.browser.go_to(search_url)

            articles = self.browser.get_webelements('//div[@class="grid__card"]')
            for article in articles:
                link = self.browser.get_element_attribute(article, 'href')
                full_link = f"https://www.annapurnapost.com{link}"
                self.links.append(full_link)
            
            self.get_data(links,keyword)
        return self.results

            # print(self.links)

    def get_data(self,links,keyword):
        
        count = 0
        for link  in links:
            try:
                self.browser.open_available_browser(link)
            except Exception as e:
                print(f"Error: {e}")
                continue
            time.sleep(5)
            # Get the article title
            title_element = self.browser.get_webelement('//h1[@class="news__title"]')

            if title_element:
                title = self.browser.get_text(title_element)
                print(f"Article Title: {title}")
            else:
                print("Error: Unable to find the title element on the page.")
            date_element = self.browser.get_webelement('//p[@class="date"]//span')
            if date_element:
                full_date = self.browser.get_text(date_element)
                print(f"Article Date: {date}")
                split_date=full_date.split()
                nep_date=split_date[1][:-1]+" "+split_date[0]+" "+split_date[2]+" "+split_date[3]
                date = date_utils.get_eng_date(nep_date)
                formated_date = f"{date[2]}-{date[1]}-{date[0]}"
                date_in_AD = nepali_datetime.date(date[2], date[1], date[0]).to_datetime_date()
            else:
                print("Error: Unable to find the date element on the page.")
            content_element = self.browser.get_webelement('//div[@class="news__details"]')
            if content_element:
                content = self.browser.get_text(content_element)
                print(f"Article Content: {content}")
            else:
                print("Error: Unable to find the content element on the page.")
            
            if(formated_date == self.nepali_date):
                    result = {}
                    result['title'] = title
                    result['link'] = link
                    result['keyword'] = keyword
                    result['date_bs'] = formated_date
                    result['date_ad'] = date_in_AD.strftime('%Y-%m-%d')
                    result['content']=content
                    result['newspaper']="Annapurna Post"
                    self.results.append(result)     
                    count += 1
                    
        print(f"Total {count} articles found for {keyword}")
        time.sleep(2)
        
    


           